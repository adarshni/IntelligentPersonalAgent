# Intelligent Personal Agent Demo

An enterprise-ready demonstration of **Agentic AI** using LangChain, Azure OpenAI, React, and Fluent UI.

![Architecture](https://img.shields.io/badge/Architecture-Agentic%20AI-blue)
![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20Fluent%20UI-purple)
![Backend](https://img.shields.io/badge/Backend-FastAPI%20%2B%20LangChain-green)
![AI](https://img.shields.io/badge/AI-Azure%20OpenAI-orange)

## 🎯 Overview

This project demonstrates how to build an **Intelligent Personal Agent** that can:

- Execute various tools based on user requests
- Maintain conversation context
- Display tool execution logs
- Provide a clean, enterprise-ready UI

## 🏗️ Architecture

```
agent-demo/
│
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py            # FastAPI application entry point
│   │   ├── config.py          # Configuration and environment variables
│   │   ├── agent_service.py   # LangChain Agent setup and execution
│   │   ├── tools.py           # Tool definitions (calculate, currency, weather, etc.)
│   │   └── schemas.py         # Pydantic request/response schemas
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment variables template
│   ├── run.sh                 # Linux/Mac startup script
│   └── run.ps1                # Windows PowerShell startup script
│
├── frontend/                   # React Vite Frontend
│   ├── src/
│   │   ├── App.jsx            # Main application component
│   │   ├── main.jsx           # React entry point with FluentProvider
│   │   ├── api.js             # Axios API client
│   │   └── components/
│   │       ├── ChatWindow.jsx     # Chat interface with messages
│   │       ├── MessageBubble.jsx  # Individual message display
│   │       └── ToolLogPanel.jsx   # Tool execution logs panel
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite configuration
│   └── index.html             # HTML entry point
│
└── README.md                   # This file
```

## 🛠️ Available Tools

The agent has access to **5 tools**:

| Tool               | Description               | Example                         |
| ------------------ | ------------------------- | ------------------------------- |
| `calculate_sum`    | Sum a list of numbers     | "What's the sum of 10, 20, 35?" |
| `convert_currency` | Convert USD/EUR/INR       | "Convert 100 USD to INR"        |
| `get_current_date` | Get current date/time     | "What's today's date?"          |
| `get_weather`      | Weather for select cities | "Weather in Bangalore"          |
| `search_web`       | Search DuckDuckGo         | "Search for AI news"            |

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.10+** installed
- **Node.js 18+** installed
- **Azure OpenAI** resource with:
  - A deployed chat model (GPT-4, GPT-4o, or GPT-3.5-turbo)
  - API key
  - Endpoint URL
  - Deployment name

## 🚀 Quick Start

### Step 1: Clone and Navigate

```bash
cd agent-demo
```

### Step 2: Configure Azure OpenAI

1. Navigate to the backend folder:

   ```bash
   cd backend
   ```

2. Copy the environment template:

   ```bash
   # Windows
   copy .env.example .env

   # Linux/Mac
   cp .env.example .env
   ```

3. Edit `.env` with your Azure OpenAI credentials:
   ```env
   AZURE_OPENAI_API_KEY=your-actual-api-key
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   ```

### Step 3: Start the Backend

**Windows (PowerShell):**

```powershell
cd backend
.\run.ps1
```

**Or manually:**

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Linux/Mac:**

```bash
cd backend
chmod +x run.sh
./run.sh
```

**Or manually:**

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

✅ Backend should be running at: **http://localhost:8000**  
📚 API Documentation: **http://localhost:8000/docs**

### Step 4: Start the Frontend

Open a **new terminal** and run:

```bash
cd frontend
npm install
npm run dev
```

✅ Frontend should be running at: **http://localhost:5173**

### Step 5: Use the Application

1. Open http://localhost:5173 in your browser
2. Try sample prompts or type your own messages
3. Watch the tool execution logs on the right panel

## 🧪 Testing the Agent

Try these example prompts:

```
1. "What's the sum of 100, 250, and 375?"
2. "Convert 500 USD to INR"
3. "What's the weather in Berlin?"
4. "What day is today?"
5. "Search the web for latest AI developments"
6. "Convert 1000 EUR to USD and add 50 to it"
```

## 🔧 API Endpoints

| Endpoint         | Method | Description                |
| ---------------- | ------ | -------------------------- |
| `/`              | GET    | Health check               |
| `/health`        | GET    | Detailed health status     |
| `/chat`          | POST   | Send message to agent      |
| `/clear-history` | POST   | Clear conversation history |
| `/tools`         | GET    | List available tools       |

### Chat Request Example

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is 10 + 20?"}'
```

### Response Example

```json
{
  "response": "The sum of 10 and 20 is 30.",
  "tool_used": "calculate_sum",
  "tool_output": "The sum of [10.0, 20.0] is 30.0",
  "thinking": "Decided to use 'calculate_sum' with input: {'numbers': [10.0, 20.0]}"
}
```

## 🎨 Features

### Frontend

- ✅ Clean enterprise UI with Fluent UI v9
- ✅ Real-time chat interface
- ✅ Loading spinners during API calls
- ✅ Tool execution logs panel
- ✅ Message history with timestamps
- ✅ Error handling and display
- ✅ Sample prompts for easy testing
- ✅ Responsive layout

### Backend

- ✅ FastAPI with async support
- ✅ LangChain Agent with tool calling
- ✅ Azure OpenAI integration
- ✅ Structured logging
- ✅ CORS configured for frontend
- ✅ Error handling
- ✅ Chat history management
- ✅ OpenAPI documentation

## 🔒 Security Notes

- Never commit your `.env` file
- Use environment variables in production
- Consider adding authentication for production use
- Review CORS settings for production deployment

## 🚢 Deployment

### Backend (Azure App Service)

1. Create an Azure App Service (Python 3.10+)
2. Set environment variables in Configuration
3. Deploy using VS Code Azure extension or Azure CLI

### Frontend (Azure Static Web Apps)

1. Build the frontend: `npm run build`
2. Deploy `dist/` folder to Azure Static Web Apps
3. Update API_BASE_URL in `api.js` to production backend URL

## 🐛 Troubleshooting

| Issue                         | Solution                                        |
| ----------------------------- | ----------------------------------------------- |
| "Unable to connect to server" | Ensure backend is running on port 8000          |
| "Configuration error"         | Check `.env` file has correct Azure credentials |
| "Module not found"            | Run `pip install -r requirements.txt`           |
| CORS errors                   | Check backend CORS settings match frontend URL  |

## 📚 Technologies Used

- **Frontend:** React 18, Vite, Fluent UI v9, Axios
- **Backend:** Python 3.10+, FastAPI, LangChain, Azure OpenAI
- **AI:** GPT-4/GPT-4o with function calling

## 📄 License

This project is for demonstration and training purposes.

---

**Happy Learning! 🤖**

_Built for Agentic AI Training_
