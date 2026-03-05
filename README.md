# 🤖 Multi-Agent Competitive Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Transform weeks of manual competitive research into minutes of AI-powered analysis using autonomous agents and enterprise-grade web scraping.

![Platform Demo](https://via.placeholder.com/800x400/1f2937/ffffff?text=Multi-Agent+Intelligence+Platform)

## 🌟 Features

- **🤖 Multi-Agent Workflow**: Three specialized AI agents working in harmony
  - 📊 **Researcher Agent**: Data collection with Bright Data web scraping
  - 🔍 **Analyst Agent**: Strategic SWOT analysis and threat assessment  
  - 📝 **Writer Agent**: Executive-ready competitive intelligence reports

- **🌊 Real-Time Streaming**: Live progress updates and tool call monitoring
- **⚡ Enterprise-Grade**: Built with FastAPI, React, and TypeScript
- **🎯 Comprehensive Analysis**: Pricing, leadership, market position, and strategy
- **📱 Beautiful UI**: Vercel-inspired design with responsive layout
- **🔧 Production Ready**: Docker support and scalable architecture

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- [Gemini API Key](https://aistudio.google.com/app/apikey)
- [Bright Data API Key](https://brightdata.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/brightdata/competitive-intelligence.git
cd competitive-intelligence
```

### 2. Backend Setup

```bash
# Install Python dependencies
cd api && pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY="your_gemini_api_key"
export BRIGHTDATA_API_KEY="your_brightdata_api_key"

# Start the API server
python app.py
```

The API will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ci-agent-ui

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 4. Try It Out!

1. Open the frontend in your browser
2. Select a demo scenario (Slack, Notion, Figma) or enter a custom company
3. Click "Start Analysis" and watch the AI agents work in real-time
4. Get comprehensive competitive intelligence in minutes!

## 📋 Table of Contents

- [Architecture](#-architecture)
- [Installation](#-installation)
- [API Documentation](#-api-documentation)
- [Frontend Guide](#-frontend-guide)
- [Configuration](#-configuration)
- [Docker Deployment](#-docker-deployment)
- [Examples](#-examples)
- [Contributing](#-contributing)
- [License](#-license)

## 🏗️ Architecture

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

                              ▲
                              │
                    ┌─────────────────┐
                    │   🌐 FastAPI    │
                    │   Backend       │
                    └─────────────────┘
                              ▲
                              │
                    ┌─────────────────┐
                    │   ⚛️ React      │
                    │   Frontend      │
                    └─────────────────┘
```

### Tech Stack

**Backend:**
- **FastAPI**: Modern, fast web framework for building APIs
- **Strands Agents**: Autonomous AI agent framework
- **Bright Data**: Enterprise web scraping and data collection
- **Google Gemini 2.0**: Advanced language model for analysis
- **LiteLLM**: Unified interface for multiple AI models

**Frontend:**
- **React 18**: Modern UI library with hooks
- **TypeScript**: Type-safe JavaScript development
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Beautiful, accessible component library

## 🛠️ Installation

### Development Setup

1. **Clone and setup backend:**
```bash
git clone https://github.com/brightdata/competitive-intelligence.git
cd competitive-intelligence

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements-api.txt
```

2. **Setup frontend:**
```bash
cd ci-agent-ui
npm install
```

3. **Environment configuration:**
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
GEMINI_API_KEY=your_gemini_api_key_here
BRIGHTDATA_API_KEY=your_brightdata_api_key_here
```

4. **Start development servers:**
```bash
# Terminal 1: Backend
python app.py

# Terminal 2: Frontend
cd ci-agent-ui && npm run dev
```

### Production Setup

See our [Docker Deployment](#-docker-deployment) section for production deployment instructions.

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Health Check
```http
GET /health
```

#### Competitive Analysis (Streaming)
```http
POST /analyze/stream
Content-Type: application/json

{
  "competitor_name": "Slack",
  "competitor_website": "https://slack.com",
  "stream": true
}
```

#### Get Demo Scenarios
```http
GET /demo-scenarios
```

#### Session Management
```http
GET /sessions
GET /sessions/{session_id}
```

### Response Format

```json
{
  "competitor": "Slack",
  "website": "https://slack.com",
  "research_findings": "Comprehensive research data...",
  "strategic_analysis": "SWOT and competitive analysis...",
  "final_report": "Executive summary and recommendations...",
  "timestamp": "2025-09-17T10:30:00Z",
  "status": "success"
}
```

### Interactive API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🎨 Frontend Guide

### Key Components

- **`CompetitiveIntelligenceForm`**: Main analysis interface with real-time streaming
- **`DemoScenarios`**: Pre-configured company examples
- **`Header`**: Navigation and branding
- **`ProgressTracker`**: Live agent workflow visualization

### Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
```

### Customization

**Styling**: Modify `tailwind.config.js` for theme customization
**Components**: Add new shadcn/ui components with `npx shadcn@latest add [component]`
**API Endpoint**: Update `API_BASE_URL` in component files

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google AI Studio API key | Yes | - |
| `BRIGHTDATA_API_KEY` | Bright Data API key | Yes | - |
| `GEMINI_MODEL_NAME` | Gemini model version | No | `gemini-2.0-flash` |
| `API_HOST` | API server host | No | `0.0.0.0` |
| `API_PORT` | API server port | No | `8000` |
| `LOG_LEVEL` | Logging level | No | `info` |

### Agent Configuration

Each agent can be customized by modifying their system prompts in `api/ci_agent.py`:

- **Researcher Agent**: Data collection and web scraping behavior
- **Analyst Agent**: Analysis depth and strategic focus
- **Writer Agent**: Report structure and formatting

## 🐳 Docker Deployment

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Docker Build

**Backend:**
```bash
cd api
docker build -t ci-backend .
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e BRIGHTDATA_API_KEY=your_key \
  ci-backend
```

**Frontend:**
```bash
cd ci-agent-ui
docker build -t ci-frontend .
docker run -p 3000:80 ci-frontend
```

### Production Considerations

- Use environment-specific configuration files
- Implement proper logging and monitoring
- Set up SSL/TLS certificates
- Configure rate limiting and security headers
- Use a reverse proxy (nginx/Cloudflare)

## 💻 Examples

### Python Client

```python
import requests

# Start streaming analysis
response = requests.post(
    "http://localhost:8000/analyze/stream",
    json={
        "competitor_name": "Slack",
        "competitor_website": "https://slack.com",
        "stream": True
    },
    stream=True
)

for line in response.iter_lines(decode_unicode=True):
    if line.startswith("data: "):
        event = json.loads(line[6:])
        print(f"Event: {event['type']}")
        
        if event['type'] == 'complete':
            print("Analysis completed!")
            break
```

### JavaScript/Fetch

```javascript
const response = await fetch('/analyze/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    competitor_name: 'Slack',
    stream: true
  })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { value, done } = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  // Process streaming events
}
```

### CLI Usage

```bash
# Run interactive demo
python api/ci_agent.py

# Analyze specific competitor
python -c "
from api.ci_agent import MultiAgentCompetitiveIntelligence
ci = MultiAgentCompetitiveIntelligence()
result = ci.run_competitive_intelligence_workflow('Slack')
print(result['final_report'])
"
```

## 🧪 Testing

### Backend Tests

```bash
cd api
pip install pytest httpx
pytest tests/
```

### Frontend Tests

```bash
cd ci-agent-ui
npm test
npm run test:coverage
```

### Integration Tests

```bash
# Start services
docker-compose up -d

# Run end-to-end tests
npm run test:e2e
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Commit with conventional commits: `git commit -m "feat: add amazing feature"`
5. Push to your fork: `git push origin feature/amazing-feature`
6. Open a Pull Request

### Code Style

- **Python**: Follow PEP 8, use Black formatter
- **TypeScript**: Follow ESLint configuration
- **Commits**: Use [Conventional Commits](https://conventionalcommits.org/)

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## 🐛 Issues and Support

- **Bug Reports**: [GitHub Issues](https://github.com/brightdata/competitive-intelligence/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/brightdata/competitive-intelligence/discussions)
- **Documentation**: [Wiki](https://github.com/brightdata/competitive-intelligence/wiki)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Strands](https://github.com/strands-ai/strands)**: Autonomous AI agent framework
- **[Bright Data](https://brightdata.com/)**: Enterprise web scraping platform
- **[Google Gemini](https://ai.google.dev/)**: Advanced language model
- **[FastAPI](https://fastapi.tiangolo.com/)**: Modern Python web framework
- **[shadcn/ui](https://ui.shadcn.com/)**: Beautiful React components

## 🔗 Links

- **Blog Post**: [Technical Deep Dive](https://dev.to/brightdata/building-multi-agent-competitive-intelligence)

---

<div align="center">

**Built with ❤️ by [Bright Data](https://github.com/brightdata)**

⭐ Star this repo if you find it useful!

</div>