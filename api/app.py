#!/usr/bin/env python3
"""
FastAPI Application for Multi-Agent Competitive Intelligence
RESTful API with streaming capabilities for real-time tool call monitoring
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from api directory so DEEPSEEK_API_KEY etc. are available
load_dotenv(Path(__file__).resolve().parent / ".env")

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import uvicorn

# Import our competitive intelligence system
from ci_agent import MultiAgentCompetitiveIntelligence, get_llm_model
from session_store import SessionStore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# CORS: comma-separated origins, e.g. http://localhost:5173,https://app.example.com
# Default allows Vite dev server and common dev ports.
_cors_origins_raw = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
CORS_ORIGINS = [o.strip() for o in _cors_origins_raw.split(",") if o.strip()]

# Persistent session store (survives restarts)
streaming_sessions = SessionStore(persist=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    logger.info("🚀 Starting Multi-Agent Competitive Intelligence API")
    
    # Test environment setup on startup
    try:
        get_llm_model()
        logger.info("✅ LLM (DeepSeek) configuration verified")
    except Exception as e:
        logger.error(f"❌ Environment setup failed: {e}")
        raise
    
    yield
    
    logger.info("🛑 Shutting down API")

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Agent Competitive Intelligence API",
    description="RESTful API for competitive intelligence analysis using specialized AI agents",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware; origins from env for production safety
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API requests/responses
class AnalysisRequest(BaseModel):
    """Request model for competitive analysis"""
    competitor_name: str = Field(..., description="Name of the competitor to analyze")
    competitor_website: Optional[str] = Field(None, description="Website URL of the competitor")
    stream: bool = Field(False, description="Enable streaming for real-time updates")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "competitor_name": "Slack",
                    "competitor_website": "https://slack.com",
                    "stream": True
                }
            ]
        }
    }

class AnalysisResponse(BaseModel):
    """Response model for completed analysis"""
    competitor: str
    website: Optional[str]
    research_findings: str
    strategic_analysis: str
    final_report: str
    timestamp: str
    status: str
    workflow: str
    session_id: Optional[str] = None

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    timestamp: str
    status: str = "error"

class StreamEvent(BaseModel):
    """Streaming event model"""
    timestamp: str
    type: str  # "status_update", "tool_call", "complete", "error"
    step: Optional[str] = None
    message: Optional[str] = None
    tool_name: Optional[str] = None
    tool_input: Optional[Dict] = None
    data: Optional[Dict] = None


def _run_workflow_sync(
    competitor_name: str,
    competitor_website: Optional[str],
    stream_callback: Any,
) -> Dict[str, Any]:
    """Run the sync multi-agent workflow (called from thread)."""
    intelligence_system = MultiAgentCompetitiveIntelligence(stream_callback)
    return intelligence_system.run_competitive_intelligence_workflow(
        competitor_name=competitor_name,
        competitor_website=competitor_website,
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Environment status endpoint
@app.get("/status")
async def get_status():
    """Get API and environment status"""
    try:
        # Test LLM (DeepSeek) connection
        get_llm_model()
        llm_status = "connected"
    except Exception as e:
        llm_status = f"error: {str(e)}"

    return {
        "api_status": "running",
        "llm_status": llm_status,
        "active_sessions": len(streaming_sessions),
        "timestamp": datetime.now().isoformat()
    }

# Non-streaming analysis endpoint
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_competitor(request: AnalysisRequest):
    """
    Perform competitive intelligence analysis

    This endpoint runs the full multi-agent workflow and returns complete results.
    For real-time updates, use the streaming endpoint.
    """
    try:
        logger.info("Starting analysis for: %s", request.competitor_name)
        # Run sync workflow in thread pool to avoid blocking the event loop
        result = await asyncio.to_thread(
            _run_workflow_sync,
            request.competitor_name,
            request.competitor_website,
            None,  # no stream callback for non-streaming
        )
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result.get("error", "Analysis failed"))
        logger.info("Analysis completed for: %s", request.competitor_name)
        return AnalysisResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Analysis failed for %s", request.competitor_name)
        raise HTTPException(status_code=500, detail=str(e))

# Streaming analysis endpoint
@app.post("/analyze/stream")
async def analyze_competitor_stream(request: AnalysisRequest):
    """
    Perform competitive intelligence analysis with real-time streaming
    
    This endpoint provides real-time updates during the analysis process,
    including tool calls, status updates, and intermediate results.
    """
    if not request.stream:
        # If streaming not requested, redirect to regular endpoint
        return await analyze_competitor(request)
    
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{request.competitor_name.replace(' ', '_')}"
    
    async def generate_stream():
        """Generate streaming events"""
        try:
            # Initialize session tracking (persisted by SessionStore)
            streaming_sessions[session_id] = {
                "start_time": datetime.now().isoformat(),
                "competitor": request.competitor_name,
                "status": "running",
            }

            events_queue: asyncio.Queue = asyncio.Queue()
            loop = asyncio.get_running_loop()

            def stream_callback(event: Dict[str, Any]) -> None:
                """Thread-safe callback: workflow runs in thread, so schedule put on main loop."""
                try:
                    json.dumps(event)
                    loop.call_soon_threadsafe(events_queue.put_nowait, event)
                except (TypeError, ValueError) as json_error:
                    safe_event = {
                        "timestamp": datetime.now().isoformat(),
                        "type": "tool_call",
                        "message": f"Non-serializable event received: {str(json_error)}",
                        "original_type": event.get("type", "unknown") if isinstance(event, dict) else "unknown",
                    }
                    loop.call_soon_threadsafe(events_queue.put_nowait, safe_event)
                except Exception as e:
                    logger.error("Stream callback error: %s", e)

            async def run_analysis() -> None:
                try:
                    # Run sync workflow in thread pool to avoid blocking the event loop
                    result = await asyncio.to_thread(
                        _run_workflow_sync,
                        request.competitor_name,
                        request.competitor_website,
                        stream_callback,
                    )

                    final_event = {
                        "timestamp": datetime.now().isoformat(),
                        "type": "complete",
                        "data": result,
                    }
                    await events_queue.put(final_event)

                    if session_id in streaming_sessions:
                        streaming_sessions[session_id]["status"] = "completed"
                        streaming_sessions[session_id]["result"] = result
                        streaming_sessions.save()
                except Exception as e:
                    logger.error("Analysis error for session %s: %s", session_id, e)
                    await events_queue.put({
                        "timestamp": datetime.now().isoformat(),
                        "type": "error",
                        "message": str(e),
                    })
                    if session_id in streaming_sessions:
                        streaming_sessions[session_id]["status"] = "error"
                        streaming_sessions.save()
                finally:
                    await events_queue.put(None)

            analysis_task = asyncio.create_task(run_analysis())
            
            # Send initial event
            initial_event = {
                "timestamp": datetime.now().isoformat(),
                "type": "session_start",
                "session_id": session_id,
                "message": f"Starting analysis for {request.competitor_name}"
            }
            yield f"data: {json.dumps(initial_event)}\n\n"
            
            # Stream events as they come
            while True:
                try:
                    # Wait for event with timeout
                    event = await asyncio.wait_for(events_queue.get(), timeout=1.0)
                    
                    if event is None:  # End of stream signal
                        break
                    
                    # Safe JSON serialization
                    try:
                        event_json = json.dumps(event)
                        yield f"data: {event_json}\n\n"
                    except (TypeError, ValueError) as e:
                        # Fallback for non-serializable events
                        safe_event = {
                            "timestamp": datetime.now().isoformat(),
                            "type": "error",
                            "message": f"Event serialization error: {str(e)}",
                            "original_type": event.get("type", "unknown")
                        }
                        yield f"data: {json.dumps(safe_event)}\n\n"
                    
                except asyncio.TimeoutError:
                    # Send heartbeat to keep connection alive
                    heartbeat = {
                        "timestamp": datetime.now().isoformat(),
                        "type": "heartbeat"
                    }
                    yield f"data: {json.dumps(heartbeat)}\n\n"
                    continue
            
            # Clean up
            await analysis_task
            
        except Exception as e:
            logger.error(f"Streaming error for session {session_id}: {e}")
            error_event = {
                "timestamp": datetime.now().isoformat(),
                "type": "error",
                "message": str(e)
            }
            yield f"data: {json.dumps(error_event)}\n\n"
        finally:
            # Clean up session after delay
            async def cleanup():
                await asyncio.sleep(300)  # Keep session for 5 minutes
                streaming_sessions.pop(session_id, None)
            
            asyncio.create_task(cleanup())
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream"
        }
    )

# Get active sessions
@app.get("/sessions")
async def get_active_sessions():
    """Get information about active streaming sessions"""
    return {
        "active_sessions": len(streaming_sessions),
        "sessions": {
            sid: {
                "start_time": data.get("start_time"),
                "competitor": data.get("competitor"),
                "status": data.get("status"),
            }
            for sid, data in streaming_sessions.items()
        },
        "timestamp": datetime.now().isoformat(),
    }

# Get session details
@app.get("/sessions/{session_id}")
async def get_session_details(session_id: str):
    """Get details for a specific session (from persistent store)."""
    if session_id not in streaming_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    data = streaming_sessions[session_id]
    # Return only JSON-serializable fields (result may contain full analysis)
    return {k: v for k, v in data.items() if isinstance(v, (str, int, float, bool, type(None), dict, list))}

# Demo scenarios endpoint
@app.get("/demo-scenarios")
async def get_demo_scenarios():
    """Get available demo scenarios for testing"""
    scenarios = [
        {
            "id": 1,
            "name": "Oxylabs",
            "website": "https://oxylabs.io",
            "description": "Data collection and web scraping"
        },
        {
            "id": 2,
            "name": "Notion",
            "website": "https://notion.so",
            "description": "All-in-one workspace"
        },
        {
            "id": 3,
            "name": "Figma",
            "website": "https://figma.com",
            "description": "Collaborative design"
        }
    ]
    
    return {
        "scenarios": scenarios,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    # Run the API server
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )