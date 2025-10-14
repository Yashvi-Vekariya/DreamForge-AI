# DreamForge AI - Setup Instructions

## Overview
DreamForge AI is a multi-agent system that transforms your ideas into production-ready code using three specialized agents:
- **Vision Agent**: Converts voice/text/sketch descriptions into structured layouts
- **Code Agent**: Generates production-ready code from layouts
- **Evaluator Agent**: Reviews and validates generated code

## Backend Setup (FastAPI)

1. Navigate to the backend directory:
```bash
cd Backand
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Copy the .env file or create one with your Groq API key
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

4. Start the FastAPI server:
```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: `http://localhost:8000`

### API Endpoints

- `GET /` - Health check
- `POST /api/vision` - Vision Agent endpoint
- `POST /api/code` - Code Agent endpoint  
- `POST /api/evaluate` - Evaluator Agent endpoint
- `POST /api/orchestrate` - Full orchestration (all agents)
- `GET /api/orchestrate-stream` - Streaming orchestration

## Frontend Setup (Next.js)

1. Navigate to the frontend directory:
```bash
cd Fronted
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at: `http://localhost:3000`

## Usage

1. **Start both servers** (backend on port 8000, frontend on port 3000)

2. **Open the frontend** in your browser at `http://localhost:3000`

3. **Enter your idea** in the input field:
   - Choose input type (voice, sketch, or text)
   - Describe your app idea, layout, or paste code to evaluate

4. **Choose your approach**:
   - **Individual Agents**: Click on specific agent cards to run them individually
   - **Full Orchestration**: Click "Run Full Orchestration" to run all agents in sequence

5. **View Results**: The results will appear below with structured output for each agent

## Example Inputs

### For Vision Agent:
- "Create a mood tracker app with emoji selection and notes"
- "Design a dashboard with charts, sidebar, and user profile"
- "Build a todo list with drag and drop functionality"

### For Code Agent:
- Paste the layout output from Vision Agent
- Or describe a specific UI layout

### For Evaluator Agent:
- Paste generated code to get feedback and suggestions

## Project Structure

```
DreamForge-AI/
├── Backand/           # FastAPI backend
│   ├── app/
│   │   ├── main.py    # FastAPI app
│   │   ├── routes.py  # API routes
│   │   └── models.py  # Pydantic models
│   └── requirements.txt
├── Fronted/           # Next.js frontend
│   ├── Pages/
│   │   ├── index.jsx  # Main page
│   │   └── _app.js    # App wrapper
│   ├── components/    # React components
│   └── styles/        # CSS styles
└── orchestrator/      # Original agents
    └── agents/        # Individual agent implementations
```

## Troubleshooting

1. **CORS Issues**: The backend is configured to allow all origins for development
2. **Port Conflicts**: Make sure ports 3000 and 8000 are available
3. **API Key**: Ensure your Groq API key is properly set in the backend .env file
4. **Dependencies**: Run `pip install -r requirements.txt` and `npm install` if you encounter import errors

## Features

- ✅ Individual agent endpoints with proper request/response models
- ✅ Full orchestration workflow
- ✅ Modern, responsive UI with Tailwind CSS
- ✅ Real-time loading states and error handling
- ✅ Code syntax highlighting and expandable results
- ✅ Streaming orchestration for real-time updates
- ✅ Integration with existing agent implementations
