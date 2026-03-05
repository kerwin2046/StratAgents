#!/usr/bin/env python3
"""
Multi-Agent Competitive Intelligence Analyzer
Strands Agents + Bright Data + DeepSeek with Multi-Agent Workflow
"""

import os
import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Union, Callable, Optional

# Load .env when running as script or when app hasn't loaded it yet
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

from strands import Agent
from strands.models.litellm import LiteLLMModel
from strands_tools import bright_data
import asyncio
from datetime import datetime

# Configure logging
logging.getLogger("strands").setLevel(logging.INFO)  # Reduced debug noise
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

def get_llm_model():
    """Configure LLM using LiteLLM (DeepSeek by default).
    Default is deepseek-chat: deepseek-reasoner requires reasoning_content in
    multi-turn/tool-call flows and is not fully compatible with Strands/LiteLLM yet.
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")
    model_name = os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat")

    if not api_key:
        raise ValueError(
            "DEEPSEEK_API_KEY not found in environment variables. "
            "Get your key at https://platform.deepseek.com/"
        )

    # LiteLLM model_id for DeepSeek: deepseek/<model-name>
    model_id = f"deepseek/{model_name}"
    print(f"🔧 Configuring LLM: {model_id}")

    model = LiteLLMModel(
        client_args={"api_key": api_key},
        model_id=model_id,
        params={"max_tokens": 4000, "temperature": 0.3},
    )
    return model

# Agent System Prompts
RESEARCHER_PROMPT = """You are a Researcher Agent specialized in competitive intelligence data gathering.

Your role:
1. **Data Collection**: Use bright_data tool to gather comprehensive competitor information
2. **Source Discovery**: Find recent news, funding announcements, product launches, and market data
3. **Website Analysis**: Scrape pricing pages, product descriptions, and company information
4. **LinkedIn Intelligence**: Get structured data about company leadership and team size

Focus on:
- Recent company developments and announcements
- Pricing strategy and product positioning
- Leadership team and company structure
- Market position and customer feedback
- Financial information (funding, revenue estimates)

Keep findings under 800 words and include source URLs.
Be thorough and systematic in data collection.
"""

ANALYST_PROMPT = """You are an Analyst Agent specialized in competitive intelligence analysis.

Your role:
1. **Strategic Analysis**: Analyze competitive positioning and market strategy
2. **SWOT Assessment**: Identify strengths, weaknesses, opportunities, and threats
3. **Business Model Analysis**: Understand revenue streams and value propositions
4. **Competitive Threats**: Assess level of competitive threat and market overlap

Focus on:
- Business model and revenue strategy analysis
- Competitive strengths and vulnerabilities
- Market positioning and differentiation
- Strategic threats and opportunities
- Key insights for competitive response

Keep analysis under 600 words with clear, actionable insights.
Rate competitive threat level from 1-5 and explain reasoning.
"""

WRITER_PROMPT = """You are a Writer Agent specialized in competitive intelligence reporting.

Your role:
1. **Executive Summary**: Create clear, actionable competitive intelligence reports
2. **Strategic Recommendations**: Provide specific recommendations based on analysis
3. **Risk Assessment**: Highlight key competitive risks and opportunities
4. **Action Items**: Suggest concrete next steps for competitive response

Structure your reports with:
- Executive Summary (key findings and threat level)
- Business Model Analysis
- Competitive Positioning
- Strategic Recommendations
- Action Items

Keep reports under 700 words, professional tone, with brief source mentions.
Focus on actionable intelligence for decision-makers.
"""

class StreamingCallbackHandler:
    """Callback handler for streaming tool calls and responses"""
    
    def __init__(self, stream_callback: Optional[Callable] = None):
        self.stream_callback = stream_callback
        
    def __call__(self, **kwargs):
        """Handle streaming callbacks"""
        if self.stream_callback:
            try:
                # Create streaming event with safe serialization
                event = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "tool_call",
                }
                
                # Safely extract tool information
                if "current_tool_use" in kwargs:
                    tool = kwargs.get("current_tool_use", {})
                    if isinstance(tool, dict):
                        event["tool_name"] = tool.get("name", "unknown")
                        # Safely serialize tool input
                        tool_input = tool.get("input", {})
                        if isinstance(tool_input, (dict, list, str, int, float, bool, type(None))):
                            event["tool_input"] = tool_input
                        else:
                            event["tool_input"] = str(tool_input)
                    elif isinstance(tool, str):
                        event["tool_name"] = tool
                        event["tool_input"] = {}
                    else:
                        event["tool_name"] = str(tool)
                        event["tool_input"] = {}
                
                # Add safe data - only include serializable items
                safe_data = {}
                for key, value in kwargs.items():
                    if key == "current_tool_use":
                        continue  # Already handled above
                    
                    # Only include JSON serializable data
                    if isinstance(value, (dict, list, str, int, float, bool, type(None))):
                        try:
                            json.dumps(value)  # Test if it's JSON serializable
                            safe_data[key] = value
                        except (TypeError, ValueError):
                            safe_data[key] = str(value)
                    else:
                        safe_data[key] = str(value)
                
                if safe_data:
                    event["data"] = safe_data
                
                # Send to stream callback
                self.stream_callback(event)
                
            except Exception as e:
                # Fallback event if something goes wrong
                error_event = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "tool_call",
                    "tool_name": "unknown",
                    "error": f"Callback error: {str(e)}"
                }
                self.stream_callback(error_event)

class MultiAgentCompetitiveIntelligence:
    """Multi-Agent Competitive Intelligence Workflow"""
    
    def __init__(self, stream_callback: Optional[Callable] = None):
        """Initialize specialized agents with enhanced error handling and streaming"""
        try:
            llm_model = get_llm_model()

            # Create callback handler for streaming
            callback_handler = StreamingCallbackHandler(stream_callback) if stream_callback else None

            # Researcher Agent with web capabilities
            self.researcher_agent = Agent(
                model=llm_model,
                system_prompt=RESEARCHER_PROMPT,
                tools=[bright_data],
                callback_handler=callback_handler
            )
            
            # Analyst Agent for competitive analysis
            self.analyst_agent = Agent(
                model=llm_model,
                system_prompt=ANALYST_PROMPT,
                callback_handler=callback_handler
            )
            
            # Writer Agent for final report creation
            self.writer_agent = Agent(
                model=llm_model,
                system_prompt=WRITER_PROMPT,
                callback_handler=callback_handler
            )
            
            self.stream_callback = stream_callback
            
            if not stream_callback:  # Only print if not in API mode
                print("✅ Multi-agent workflow initialized successfully!")
                print("   📊 Researcher Agent: Data gathering and web scraping")
                print("   🔍 Analyst Agent: Strategic analysis and threat assessment") 
                print("   📝 Writer Agent: Report generation and recommendations")
            
        except Exception as e:
            if not stream_callback:
                print(f"❌ Multi-agent initialization failed: {e}")
            raise
    
    def _send_status_update(self, message: str, step: str = "info"):
        """Send status update through stream if available"""
        if self.stream_callback:
            event = {
                "timestamp": datetime.now().isoformat(),
                "type": "status_update",
                "step": step,
                "message": message
            }
            self.stream_callback(event)
        else:
            print(message)

    def run_competitive_intelligence_workflow(self, competitor_name: str, competitor_website: str = None) -> Dict[str, Any]:
        """
        Multi-agent competitive intelligence workflow
        """
        self._send_status_update(f"\n🎯 Starting Multi-Agent Analysis for: {competitor_name}", "start")
        self._send_status_update("=" * 60)
        
        try:
            # Step 1: Researcher Agent gathers comprehensive data
            self._send_status_update("\n📊 Step 1: Researcher Agent gathering competitive intelligence...", "research_start")
            
            research_query = f"""Research competitive intelligence for "{competitor_name}".
            
            {'Website: ' + competitor_website if competitor_website else ''}
            
            Gather comprehensive information about:
            1. Recent company news, funding, and market developments
            2. Pricing strategy and product positioning (scrape pricing pages)
            3. Company leadership and team structure (LinkedIn data)
            4. Market position and customer feedback
            5. Financial information and growth metrics
            
            Use your tools to collect detailed, factual information from multiple sources.
            """
            
            researcher_response = self.researcher_agent(research_query)
            research_findings = str(researcher_response)
            self._send_status_update("✅ Research complete", "research_complete")
            
            # Step 2: Analyst Agent performs strategic analysis
            self._send_status_update("\n🔍 Step 2: Analyst Agent performing strategic analysis...", "analysis_start")
            self._send_status_update("Analyzing competitive positioning and threats...")
            
            analysis_query = f"""Analyze these competitive intelligence findings for "{competitor_name}":

            {research_findings}
            
            Provide strategic analysis including:
            1. SWOT assessment (strengths, weaknesses, opportunities, threats)
            2. Business model and revenue strategy analysis
            3. Competitive positioning and market differentiation
            4. Assessment of competitive threat level (rate 1-5)
            5. Key strategic insights for competitive response
            
            Focus on actionable insights and strategic implications.
            """
            
            analyst_response = self.analyst_agent(analysis_query)
            strategic_analysis = str(analyst_response)
            self._send_status_update("✅ Strategic analysis complete", "analysis_complete")
            
            # Step 3: Writer Agent creates final report
            self._send_status_update("\n📝 Step 3: Writer Agent generating comprehensive report...", "report_start")
            
            report_query = f"""Create a comprehensive competitive intelligence report for "{competitor_name}" based on this analysis:

            RESEARCH FINDINGS:
            {research_findings}
            
            STRATEGIC ANALYSIS:
            {strategic_analysis}
            
            Generate a professional report with:
            - Executive Summary (key findings and threat assessment)
            - Business Model Analysis
            - Competitive Positioning
            - Strategic Recommendations
            - Action Items for competitive response
            
            Focus on actionable intelligence for decision-makers.
            """
            
            final_report = self.writer_agent(report_query)
            
            self._send_status_update("\n" + "=" * 60, "complete")
            self._send_status_update("✅ Multi-Agent Analysis Complete!", "complete")
            self._send_status_update("=" * 60)
            
            # Return comprehensive results
            return {
                "competitor": competitor_name,
                "website": competitor_website,
                "research_findings": research_findings,
                "strategic_analysis": strategic_analysis,
                "final_report": str(final_report),
                "timestamp": datetime.now().isoformat(),
                "status": "success",
                "workflow": "multi_agent"
            }
            
        except Exception as e:
            error_msg = str(e)
            self._send_status_update(f"\n❌ Multi-agent workflow failed: {error_msg}", "error")
            
            # Return error with any partial results
            return {
                "competitor": competitor_name,
                "website": competitor_website,
                "error": error_msg,
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "workflow": "multi_agent"
            }

def safe_get(dictionary: Union[Dict, str, Any], key: str, default: Any = None) -> Any:
    """Safely get value from dictionary, handling edge cases"""
    if isinstance(dictionary, dict):
        return dictionary.get(key, default)
    else:
        return default

def main():
    """Main demo function with multi-agent workflow"""
    
    print("🚀 Multi-Agent Competitive Intelligence Demo")
    print("   Strands Agents + Bright Data + Gemini")
    print("=" * 70)
    
    try:
        print("\n🔧 Initializing multi-agent workflow...")
        intelligence_system = MultiAgentCompetitiveIntelligence()
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nRequired Environment Variables:")
        print("- DEEPSEEK_API_KEY: Your DeepSeek API key")
        print("- BRIGHTDATA_API_KEY: Your Bright Data API key")
        print("\nGet DeepSeek API key: https://platform.deepseek.com/")
        return
    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        return
    
    demo_scenarios = [
        {"name": "Oxylabs", "website": "https://oxylabs.io", "description": "Enterprise communication"},
        {"name": "Notion", "website": "https://notion.so", "description": "All-in-one workspace"},
        {"name": "Figma", "website": "https://figma.com", "description": "Collaborative design"}
    ]
    
    print("\nDemo Scenarios (Multi-Agent Workflow):")
    for i, scenario in enumerate(demo_scenarios, 1):
        print(f"{i}. {scenario['name']} - {scenario['description']}")
    
    print("\nOptions:")
    print("- Enter 1-3 to run a demo scenario with multi-agent workflow")
    print("- Enter custom company name for multi-agent analysis")
    print("- Enter 'quit' to exit")
    print("\n🤖 Each analysis uses 3 specialized agents:")
    print("   📊 Researcher → 🔍 Analyst → 📝 Writer")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
                
            elif user_input in ['1', '2', '3']:
                scenario = demo_scenarios[int(user_input) - 1]
                result = intelligence_system.run_competitive_intelligence_workflow(
                    scenario['name'], 
                    scenario['website']
                )
                
                # Display multi-agent results
                if safe_get(result, 'status') == 'success':
                    print(f"\n📊 Multi-Agent Analysis Summary for {safe_get(result, 'competitor', 'Unknown')}:")
                    print("-" * 50)
                    print(f"Workflow: {safe_get(result, 'workflow', 'Unknown')}")
                    print(f"Generated at: {safe_get(result, 'timestamp', 'Unknown time')}")
                    
                    # Show final report preview
                    final_report = safe_get(result, 'final_report', '')
                    if final_report and len(final_report) > 300:
                        print(f"\n📝 Final Report Preview:\n{final_report}")
                        print(f"\n💡 Tip: Full analysis includes research findings, strategic analysis, and comprehensive report")
                    elif final_report:
                        print(f"\n📝 Final Report:\n{final_report}")
                else:
                    error = safe_get(result, 'error', 'Unknown error')
                    print(f"\n❌ Multi-agent analysis failed: {error}")
                
            else:
                # Custom competitor analysis
                competitor_name = user_input
                result = intelligence_system.run_competitive_intelligence_workflow(competitor_name)
                
                if safe_get(result, 'status') == 'success':
                    print(f"\n📊 Multi-agent analysis completed for {competitor_name}")
                    final_report = safe_get(result, 'final_report', '')
                    if final_report and len(final_report) > 200:
                        print(f"\n📝 Report Preview:\n{final_report}")
                    elif final_report:
                        print(f"\n📝 Report:\n{final_report}")
                else:
                    error = safe_get(result, 'error', 'Unknown error')
                    print(f"\n❌ Multi-agent analysis failed: {error}")
                    
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted by user")
            break
        except Exception as e:
            print(f"\n⚠️  Unexpected error: {e}")
            print("Continuing...")
    
    print("\n👋 Demo completed!")

if __name__ == "__main__":
    main()