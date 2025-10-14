# 🚀 DreamForge AI - Usage Guide

## ✅ System Status
Your DreamForge AI multi-agent system is now **FULLY OPERATIONAL**!

- **Backend API**: ✅ Running on http://localhost:8000
- **Frontend UI**: ✅ Running on http://localhost:3000
- **All 3 Agents**: ✅ Vision, Code, and Evaluator agents working
- **Full Orchestration**: ✅ All agents working together

## 🎯 How to Use

### 1. **Access the Web Interface**
Open your browser and go to: **http://localhost:3000**

### 2. **Using Individual Agents**

#### 🔵 Vision Agent
- **Purpose**: Converts your ideas into structured UI layouts
- **Input**: Describe your app idea (voice, sketch, or text description)
- **Example**: "Create a todo list app with add, edit, and delete functionality"
- **Output**: Structured layout description with components and data elements

#### 🟢 Code Agent  
- **Purpose**: Generates production-ready code from layouts
- **Input**: Layout description (from Vision Agent or manual input)
- **Example**: "Dashboard with header, sidebar, main content, and footer"
- **Output**: Complete React/Vue/Angular code

#### 🟣 Evaluator Agent
- **Purpose**: Reviews and validates generated code
- **Input**: Generated code (from Code Agent or manual input)
- **Example**: Paste any React component code
- **Output**: Code review with issues, suggestions, and feedback

### 3. **Full Orchestration Workflow**
Click **"🎯 Run Full Orchestration"** to run all three agents in sequence:
1. Vision Agent processes your idea
2. Code Agent generates code from the layout
3. Evaluator Agent reviews the generated code
4. Get complete results from all agents

## 📋 Sample Inputs to Try

### For Vision Agent:
```
Input Type: Voice
Description: Create a weather app with current conditions, 5-day forecast, and location search
```

```
Input Type: Text  
Description: Build a social media dashboard with posts, comments, likes, and user profiles
```

### For Code Agent:
```
Layout: Simple login form with email, password fields, and submit button
Framework: React
```

### For Evaluator Agent:
```javascript
function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  return (
    <form>
      <input type="email" value={email} onChange={e => setEmail(e.target.value)} />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button type="submit">Login</button>
    </form>
  );
}
```

## 🔧 API Endpoints (for developers)

### Individual Agents:
- `POST /api/vision` - Vision Agent
- `POST /api/code` - Code Agent  
- `POST /api/evaluate` - Evaluator Agent

### Orchestration:
- `POST /api/orchestrate` - Full orchestration
- `GET /api/orchestrate-stream` - Streaming orchestration

### Documentation:
- `GET /docs` - Interactive API documentation

## 🧪 Testing

### Test Backend Only:
```bash
cd backend
source venv/bin/activate
python3 test_api.py
```

### Test Full Stack:
```bash
python3 test_full_stack.py
```

## 🎨 Features

### ✨ Modern UI
- Beautiful gradient backgrounds
- Glass-morphism effects  
- Responsive design
- Real-time loading states
- Error handling

### 🔄 Agent Integration
- Individual agent calls
- Full orchestration workflow
- Streaming responses
- Result visualization

### 📊 Result Display
- Structured output for each agent
- Syntax highlighting for code
- Expandable/collapsible results
- Success/failure indicators

## 🚀 Advanced Usage

### Custom Frameworks
The Code Agent supports multiple frameworks:
- React (default)
- Vue.js
- Angular

### Input Types
The Vision Agent accepts:
- Voice descriptions
- Sketch descriptions  
- Text descriptions

### Streaming Mode
For real-time updates, use the streaming orchestration endpoint.

## 🎉 You're All Set!

Your DreamForge AI system is ready to transform ideas into production-ready code. Start by opening http://localhost:3000 and experimenting with different inputs!

**Happy coding!** 🚀
