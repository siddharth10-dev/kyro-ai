# Kyro

<div align="center">
  <img src="https://img.shields.io/badge/Status-Active-success" alt="Status" />
  <img src="https://img.shields.io/badge/Platform-Enterprise-blue" alt="Platform" />
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License" />
</div>

<br />

**Kyro** is an Enterprise AI-powered Incident Response Platform. 
It operates completely autonomously, bridging the gap between monitoring systems and incident resolution by leveraging Large Language Models (LLMs) and intelligent agent orchestration.

Think of how Datadog + Prometheus + Alertmanager + PagerDuty work together. Kyro sits on top of these tools, catching alerts, running autonomous investigations, pulling logs, reading runbooks, and compiling executive resolutions before you even wake up.

---

## 🌟 Key Features

- **Event-Driven Architecture**: Native integrations with Prometheus and Alertmanager via webhooks.
- **Autonomous Investigation**: LangGraph-powered agents execute dynamic investigations without human intervention.
- **Log Aggregation & Analysis**: Agents can securely fetch and analyze application logs to pinpoint root causes.
- **Runbook Execution**: Automatically fetches relevant internal runbooks to determine the best resolution.
- **Executive Summaries**: Drafts clear, concise incident reports and Slack messages for stakeholders.
- **Glassmorphic UI**: A stunning, high-performance Vite + React frontend dashboard featuring real-time telemetry, skeleton loaders, and interactive components.

---

## 🏗 System Architecture

```mermaid
graph TD
    %% Define Styles
    classDef client fill:#1E293B,stroke:#3B82F6,stroke-width:2px,color:#fff;
    classDef microservice fill:#0F172A,stroke:#10B981,stroke-width:2px,color:#fff;
    classDef monitoring fill:#374151,stroke:#F59E0B,stroke-width:2px,color:#fff;
    classDef kyro fill:#090D16,stroke:#8B5CF6,stroke-width:3px,color:#fff;
    classDef database fill:#111827,stroke:#6366F1,stroke-width:2px,color:#fff;

    %% Nodes
    User([Customer]):::client
    Checkout[Checkout Service<br/>(API Gateway)]:::microservice
    
    Prometheus[(Prometheus<br/>Metrics Engine)]:::monitoring
    AlertManager[Alertmanager<br/>(Routing)]:::monitoring
    
    KyroBackend[Kyro Backend<br/>(FastAPI)]:::kyro
    Agents((LangGraph Agents<br/>AI Reasoning)):::kyro
    DB[(PostgreSQL<br/>Incidents & Telemetry)]:::database
    Frontend[Kyro Command Center<br/>(React UI)]:::kyro

    %% Connections
    User -->|Initiates Request| Checkout
    Checkout -->|Emits Metrics| Prometheus
    Prometheus -->|Threshold Breach| AlertManager
    AlertManager -->|Webhook| KyroBackend
    KyroBackend -->|Spawns Graph| Agents
    Agents <-->|Fetch Logs & Runbooks| Checkout
    Agents -->|Persists Data| DB
    KyroBackend <-->|Real-time state| DB
    Frontend <-->|REST / Polling| KyroBackend
```

---

## 🛠 Tech Stack

- **Frontend**: React 19, Vite, TailwindCSS (Vanilla CSS config), Framer Motion, Recharts, Lucide React.
- **Backend**: Python 3.10+, FastAPI, LangChain, LangGraph, SQLAlchemy, PostgreSQL, Uvicorn.
- **Monitoring**: Prometheus, Alertmanager, Docker Compose.
- **LLMs**: Gemini via `gemini-2.5-flash` / `gemini-2.0-flash` for high-speed, cost-effective reasoning.

---

## 📂 Project Structure

```bash
kyro/
├── backend/                  # FastAPI & LangGraph AI Backend
│   ├── app/
│   │   ├── api/              # REST Endpoints
│   │   ├── core/             # AI Agent Workflow (LangGraph)
│   │   ├── tools/            # Tools (Logs, Runbooks, Exec Summaries)
│   │   └── database.py       # SQLAlchemy Models
│   ├── requirements.txt      
│   └── .env                  # Backend Secrets
├── frontend/                 # React Command Center
│   ├── src/
│   │   ├── components/       # IncidentDetails, Dashboard, UI
│   │   ├── utils/            # formatTime, api handlers
│   │   └── pages/            # Application Views
│   └── tailwind.config.js    
├── services/                 # Mock Microservices
│   └── checkout-service/     # Simulated Checkout App + Mock Endpoints
├── prometheus.yml            # Prometheus Scraping config
├── alertmanager.yml          # Alertmanager Webhook config
└── docker-compose.yml        # Dockerized dependencies (Postgres, Prom, Alertmanager)
```

---

## 🚀 Setup Instructions

Follow these steps to run Kyro locally for development and testing.

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Node.js 18+
- Gemini API Key

### 2. Infrastructure (Docker)
Start the foundational infrastructure including PostgreSQL, Prometheus, and Alertmanager.
```bash
docker-compose up -d --build
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Create a `.env` file in the `backend/` directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://localhost:5432/kyro
```
Run the FastAPI backend:
```bash
PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. Checkout Service (Simulated Environment)
The checkout service provides the logs, mock metrics, and runbooks required for Kyro to investigate.
```bash
cd services/checkout-service
PYTHONPATH=. ../../backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### 5. Frontend Command Center
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 🧪 Simulation & Testing

You can use the **Simulation Control Panel** inside the Frontend UI to inject faults into the `checkout-service`. 

1. Navigate to the Dashboard.
2. Click **⚡ Simulation Control Panel**.
3. Trigger a simulation (e.g. *Database Failure*, *High Latency*, *CPU Spike*).
4. Watch the timeline populate automatically as Prometheus catches the anomaly, alerts Kyro, and the LangGraph agents begin their investigation.

---

## 🔮 Future Improvements

- **Jira & Slack Integration**: Add native OAuth capabilities to post directly into #incident-channels.
- **WebSocket Streaming**: Replace rapid polling with WebSockets for true real-time event streaming from LangGraph to the frontend.
- **Runbook Editor**: Allow SRE teams to write and manage runbooks natively within the Kyro UI.
- **Predictive Analytics**: Use historical incident data to predict when system resources might fail before they hit critical thresholds.

---

<div align="center">
  <b>Built for SREs, by AI.</b>
</div>
