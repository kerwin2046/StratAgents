# Multi-Agent Competitive Intelligence API

A FastAPI-based RESTful API for competitive intelligence analysis using specialized AI agents with real-time streaming capabilities.

## Features

- **🤖 Multi-Agent Workflow**: Three specialized agents (Researcher, Analyst, Writer)
- **🌊 Real-time Streaming**: Live updates during analysis with tool call monitoring
- **📊 Comprehensive Analysis**: Research findings, strategic analysis, and executive reports
- **🔗 RESTful API**: Standard HTTP endpoints with JSON responses
- **📝 Interactive Documentation**: Auto-generated OpenAPI/Swagger docs
- **🎯 Session Management**: Track and monitor active analysis sessions

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   📊 Researcher │───▶│   🔍 Analyst    │───▶│   📝 Writer     │
│     Agent       │    │     Agent       │    │     Agent       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
   Data Collection      Strategic Analysis       Report Generation
   - Web scraping       - SWOT analysis         - Executive summary
   - Market research     - Threat assessment     - Recommendations
   - Company intel       - Competitive position  - Action items
```

## Quick Start

### 1. Install Dependencies

```bash
# Install FastAPI and related dependencies
pip install -r requirements-api.txt

# Ensure your existing strands environment is set up
# (strands, strands-tools, litellm should already be installed)
```

### 2. Set Environment Variables

```bash
export DEEPSEEK_API_KEY="your_deepseek_api_key"
export BRIGHTDATA_API_KEY="your_brightdata_api_key"
```

Or copy `.env.example` to `.env` and fill in your keys (requires `python-dotenv`).

### 3. Start the API Server

```bash
# Development mode with auto-reload
python app.py

# Or using uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access the API

- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## API Endpoints

### Core Endpoints

#### `GET /health`
Health check endpoint
```json
{
  "status": "healthy",
  "timestamp": "2025-09-11T10:30:00Z",
  "version": "1.0.0"
}
```

#### `GET /status`
Get API and environment status
```json
{
  "api_status": "running",
  "llm_status": "connected",
  "active_sessions": 2,
  "timestamp": "2025-09-11T10:30:00Z"
}
```

#### `POST /analyze`
Perform competitive analysis (non-streaming)
```json
{
  "competitor_name": "Slack",
  "competitor_website": "https://slack.com",
  "stream": false
}
```

#### `POST /analyze/stream`
Perform competitive analysis with streaming updates
```json
{
  "competitor_name": "Slack",
  "competitor_website": "https://slack.com",
  "stream": true
}
```

### Session Management

#### `GET /sessions`
Get active streaming sessions
```json
{
  "active_sessions": 1,
  "sessions": {
    "session_20250911_103000_Slack": {
      "start_time": "2025-09-11T10:30:00Z",
      "competitor": "Slack",
      "status": "running"
    }
  }
}
```

#### `GET /sessions/{session_id}`
Get details for a specific session

### Demo & Testing

#### `GET /demo-scenarios`
Get predefined demo scenarios for testing
```json
{
  "scenarios": [
    {
      "id": 1,
      "name": "Oxylabs",
      "website": "https://oxylabs.io",
      "description": "Data collection and web scraping"
    }
  ]
}
```

## Streaming Events

The streaming endpoint (`/analyze/stream`) provides real-time updates through Server-Sent Events (SSE):

### Event Types

1. **session_start**: Analysis session initiated
2. **status_update**: Progress updates (research_start, analysis_start, etc.)
3. **tool_call**: Real-time tool execution notifications
4. **complete**: Analysis finished with full results
5. **error**: Error occurred during analysis
6. **heartbeat**: Keep-alive signals

### Example Stream Event
```json
{
  "timestamp": "2025-09-11T10:30:00Z",
  "type": "tool_call",
  "tool_name": "bright_data",
  "tool_input": {
    "action": "web_search",
    "query": "Slack company news 2025"
  }
}
```

## Usage Examples

### Python Client

```python
import requests

# Non-streaming analysis
response = requests.post("http://localhost:8000/analyze", json={
    "competitor_name": "Slack",
    "competitor_website": "https://slack.com"
})
result = response.json()

# Streaming analysis
response = requests.post(
    "http://localhost:8000/analyze/stream",
    json={"competitor_name": "Slack", "stream": True},
    stream=True
)

for line in response.iter_lines(decode_unicode=True):
    if line.startswith("data: "):
        event = json.loads(line[6:])
        print(f"Event: {event['type']}")
```

### JavaScript/Frontend

```javascript
// Streaming with EventSource
const eventSource = new EventSource('/analyze/stream');

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Event:', data.type, data.message);
    
    if (data.type === 'complete') {
        console.log('Analysis completed:', data.data);
        eventSource.close();
    }
};
```

### cURL Examples

```bash
# Health check
curl http://localhost:8000/health

# Non-streaming analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"competitor_name": "Slack", "competitor_website": "https://slack.com"}'

# Streaming analysis
curl -X POST http://localhost:8000/analyze/stream \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"competitor_name": "Slack", "stream": true}'
```

## Client Example

Run the provided client example:

```bash
python api_client_example.py
```

This demonstrates:
- Non-streaming analysis
- Streaming analysis with real-time updates
- Session management
- Error handling

## Response Schema

### Analysis Response
```json
{
  "competitor": "string",
  "website": "string",
  "research_findings": "string",
  "strategic_analysis": "string", 
  "final_report": "string",
  "timestamp": "string",
  "status": "success",
  "workflow": "multi_agent",
  "session_id": "string"
}
```

### Error Response
```json
{
  "error": "string",
  "timestamp": "string",
  "status": "error"
}
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest httpx

# Run tests (create test files as needed)
pytest tests/
```

### Development Mode

```bash
# Run with auto-reload
uvicorn app:app --reload --log-level debug

# Or use the built-in development server
python app.py
```

## Production Deployment

### Environment Configuration

```bash
# Production environment variables
export ENVIRONMENT=production
export API_HOST=0.0.0.0
export API_PORT=8000
export LOG_LEVEL=info

# Security
export ALLOWED_ORIGINS="https://yourdomain.com"
export API_KEY_HEADER="X-API-Key"  # Optional API key authentication
```

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements-api.txt .
RUN pip install -r requirements-api.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Performance Considerations

- **Concurrent Requests**: FastAPI handles multiple requests concurrently
- **Session Cleanup**: Streaming sessions are automatically cleaned up after 5 minutes
- **Memory Management**: Large analysis results are streamed to prevent memory issues
- **Rate Limiting**: Consider implementing rate limiting for production use

## Frontend Integration

The API is designed to work with modern frontend frameworks:

- **React/Vue/Angular**: Use EventSource or fetch for streaming
- **WebSocket Alternative**: SSE provides simpler real-time updates
- **CORS Enabled**: Ready for cross-origin requests (configure for production)

Example frontend integration coming soon!

## Troubleshooting

### Common Issues

1. **Environment Variables**: Ensure DEEPSEEK_API_KEY and BRIGHTDATA_API_KEY are set
2. **Dependencies**: Make sure strands and related packages are installed
3. **Port Conflicts**: Default port 8000, change if needed
4. **Streaming Issues**: Check firewall/proxy settings for SSE support

### Logs

Check logs for detailed error information:
```bash
# Application logs show in console when running
python app.py

# Or with uvicorn
uvicorn app:app --log-level debug
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## License

[Your license here]