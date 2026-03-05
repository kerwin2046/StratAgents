# Competitive Intelligence Frontend

A beautiful, Vercel-inspired React frontend for the Multi-Agent Competitive Intelligence API.

## Features

- 🎨 **Modern Design**: Clean, minimal interface inspired by Vercel
- 🔄 **Real-time Streaming**: Live updates during analysis with progress tracking
- 🤖 **Multi-Agent Visualization**: Shows progress through Researcher → Analyst → Writer workflow
- 📱 **Responsive**: Works perfectly on desktop and mobile
- ⚡ **Fast**: Built with Vite + React + TypeScript
- 🎯 **Demo Scenarios**: Pre-configured company examples for quick testing

## Tech Stack

- **Frontend**: Vite + React + TypeScript
- **UI**: shadcn/ui components
- **Styling**: Tailwind CSS
- **Forms**: React Hook Form + Zod validation
- **Icons**: Lucide React

## Quick Start

### 1. Start the Backend API

First, make sure your backend API is running:

```bash
# From the main directory
cd /path/to/competitive-intelligence
python app.py
```

The API should be available at `http://localhost:8000`

### 2. Start the Frontend

```bash
# Navigate to the frontend directory
cd ci-agent-ui

# Install dependencies (if not already done)
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

### 1. **Enter Company Details**
   - Company Name (required): e.g., "Slack", "Notion", "Figma"
   - Company URL (optional): e.g., "https://slack.com"

### 2. **Try Demo Scenarios**
   - Click any demo scenario card to auto-fill the form
   - Pre-configured with popular companies for testing

### 3. **Start Analysis**
   - Click "Start Analysis" to begin the multi-agent workflow
   - Watch real-time progress as agents work through:
     - 📊 **Researcher Agent**: Data collection and web scraping
     - 🔍 **Analyst Agent**: Strategic analysis and SWOT assessment
     - 📝 **Writer Agent**: Report generation and recommendations

### 4. **View Results**
   - Executive summary with actionable insights
   - Detailed research findings (expandable)
   - Strategic analysis (expandable)
   - Download or start new analysis

## Components

### Main Components

- **`CompetitiveIntelligenceForm`**: Main form and analysis interface
- **`DemoScenarios`**: Pre-configured demo companies
- **`Header`**: Navigation and branding

### UI Components (shadcn/ui)

- **Forms**: Input, Label, Button with validation
- **Layout**: Card, Separator for structure
- **Feedback**: Progress, Badge, Alert for status
- **Data**: Collapsible sections for detailed results

## API Integration

The frontend connects to the backend API at `http://localhost:8000`:

### Endpoints Used

- `POST /analyze/stream`: Streaming analysis with real-time updates
- `GET /demo-scenarios`: Available demo companies
- `GET /health`: API health check

### Streaming Events

The frontend handles these event types from the API:

- `session_start`: Analysis begins
- `status_update`: Progress updates (research_start, analysis_start, etc.)
- `tool_call`: Real-time tool execution
- `complete`: Analysis finished with results
- `error`: Error handling
- `heartbeat`: Connection keep-alive

## Development

### Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
```

### Adding New Components

```bash
# Add shadcn/ui components
npx shadcn@latest add [component-name]

# Example: Add a new dialog component
npx shadcn@latest add dialog
```

### Environment Variables

The frontend automatically connects to `http://localhost:8000`. To change this:

1. Create a `.env.local` file
2. Add: `VITE_API_BASE_URL=http://your-api-url:port`
3. Update the `API_BASE_URL` constant in `CompetitiveIntelligenceForm.tsx`

## Design Principles

### Vercel-Inspired Aesthetics

- **Clean**: Minimal design with lots of white space
- **Typography**: Clear hierarchy with proper font weights
- **Colors**: Subtle grays with strategic use of color for status
- **Shadows**: Soft shadows for depth and layering
- **Animations**: Smooth transitions and loading states

### User Experience

- **Progressive Disclosure**: Results expand to show more detail
- **Real-time Feedback**: Live progress and status updates
- **Error Handling**: Clear error messages with recovery options
- **Mobile First**: Responsive design that works on all devices

## Customization

### Styling

All styles use Tailwind CSS classes. Key customizations:

- **Colors**: Modify in `tailwind.config.js` or use CSS variables
- **Typography**: Update font settings in the config
- **Spacing**: Adjust the spacing scale for your needs

### Components

- **Form Validation**: Modify the `formSchema` in `CompetitiveIntelligenceForm.tsx`
- **Demo Scenarios**: Update the scenarios in `DemoScenarios.tsx`
- **Branding**: Change logos and text in `Header.tsx`

## Production Build

```bash
# Build for production
npm run build

# Preview the build
npm run preview

# Deploy the dist/ folder to your hosting provider
```

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Ensure backend is running on `http://localhost:8000`
   - Check browser console for CORS errors
   - Verify API health at `http://localhost:8000/health`

2. **Streaming Not Working**
   - Check that your browser supports Server-Sent Events
   - Verify network/firewall settings allow streaming connections
   - Look for errors in browser developer tools

3. **Build Errors**
   - Run `npm install` to ensure all dependencies are installed
   - Check TypeScript errors with `npm run lint`
   - Clear node_modules and reinstall if needed

### Performance

- The frontend uses React's built-in optimizations
- Streaming events are handled efficiently with controlled state updates
- Large analysis results are displayed progressively

## Contributing

1. Follow the existing code style
2. Use TypeScript for all new components
3. Add proper error handling
4. Test on both desktop and mobile
5. Update documentation for new features