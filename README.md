# Sentinel AI

## Multi-Agent AI Incident Response Platform

Sentinel AI is an AI-powered incident response system that helps engineering teams investigate production issues faster.

The platform receives alerts from monitoring systems, collects operational evidence, analyzes possible root causes, retrieves relevant recovery procedures, and generates recommended actions through a multi-agent workflow.

It combines backend engineering, AI agents, tool calling, retrieval systems, and human-in-the-loop decision making.

---

## System Architecture

```
Incoming Alert
(PagerDuty / Webhook)

        ↓

Alert Agent
(Normalization + Classification)

        ↓

Investigation Agent
(Log, Metrics & Deployment Analysis)

        ↓

Root Cause Agent
(Reasoning + Hypothesis Generation)

        ↓

Runbook Agent
(Semantic Knowledge Retrieval)

        ↓

Recommendation Agent
(Action Plan + Risk Analysis)

        ↓

Human Approval

        ↓

Communication Agent
(Reports + Slack Updates)
```

---

## How It Works

### 1. Alert Agent

The Alert Agent is responsible for processing incoming incidents.

It converts raw monitoring alerts into structured incidents by identifying:

- affected service
- incident category
- severity level
- priority

Example:

Input

```json
{
  "service": "payment-api",
  "message": "500 errors detected after deployment",
  "severity": "critical"
}
```

Output

```json
{
  "category": "backend-error",
  "priority": "P1"
}
```

---

## 2. Investigation Agent

The Investigation Agent gathers evidence required for debugging.

It follows an agentic reasoning workflow:

```
Analyze Problem
        ↓
Choose Tool
        ↓
Execute Tool
        ↓
Observe Results
        ↓
Continue Investigation
```

Integrated tools:

- Application log analysis
- System metrics inspection
- Database health checks
- GitHub deployment analysis

Example:

```
Incident:
High API failures detected

Investigation:

Logs:
Database connection timeout errors

Metrics:
Connection pool usage exceeded threshold

Recent Deployment:
Configuration change detected
```

---

## 3. Root Cause Agent

The Root Cause Agent analyzes collected evidence and identifies the most likely failure reason.

Responsibilities:

- correlate multiple signals
- generate hypotheses
- estimate confidence levels
- explain reasoning

Example:

```json
{
  "root_cause": "Database connection pool exhaustion after deployment configuration change",

  "confidence": 0.91
}
```

---

## 4. Runbook Agent

The Runbook Agent provides recovery knowledge using Retrieval Augmented Generation.

It searches previous incidents, documentation, and operational guides.

Pipeline:

```
Incident Context

      ↓

Generate Embedding

      ↓

Vector Search

      ↓

Retrieve Similar Fixes

      ↓

Generate Solution Context
```

Powered by:

- Vector embeddings
- PostgreSQL
- pgvector
- Semantic search

---

## 5. Recommendation Agent

The Recommendation Agent converts analysis into an actionable recovery plan.

Generated output includes:

- recommended fixes
- impact assessment
- risk level
- rollback suggestions


Example:

```json
{
  "recommended_actions": [

    "Increase database connection pool limit",

    "Restart affected API instances",

    "Monitor latency metrics"

  ],

  "risk": "medium"
}
```

---

## 6. Human Approval System

Sentinel AI keeps engineers in control.

Before execution or communication, recommendations pass through an approval workflow.

Supported actions:

- Approve
- Modify
- Reject

---

## 7. Communication Agent

After approval, the Communication Agent generates incident reports and updates teams.

Features:

- Slack notifications
- Incident summaries
- Resolution reports

---

# Tech Stack

## Backend

- Python
- FastAPI
- PostgreSQL
- Redis
- Celery
- REST APIs

## AI System

- LangGraph
- OpenAI API
- Agentic Workflows
- Function Calling
- Retrieval Augmented Generation (RAG)
- Vector Databases

## Infrastructure

- Docker
- GitHub Actions
- Cloud Deployment

## Frontend

- React
- Tailwind CSS


---

# Project Structure

```
sentinel-ai/


backend/

 ├── app/

 │    ├── agents/

 │    │      ├── alert_agent.py

 │    │      ├── investigation_agent.py

 │    │      ├── root_cause_agent.py

 │    │      ├── runbook_agent.py

 │    │      └── recommendation_agent.py


 │    ├── tools/

 │    │      ├── logs.py

 │    │      ├── metrics.py

 │    │      ├── github.py

 │    │      └── database_health.py


 │    ├── database/

 │    ├── schemas/

 │    ├── workers/

 │    └── main.py


frontend/

docker-compose.yml

README.md
```

---

# API Example

Endpoint:

```
POST /incident
```


Request:

```json
{
  "service": "payment-api",
  "message": "API returning 500 errors",
  "severity": "critical"
}
```


Response:

```json
{
  "incident_id": "INC-102",

  "root_cause":
  "Database connection exhaustion",

  "confidence": 0.91,

  "recommendation":
  "Increase connection pool size and restart affected service"
}
```

---

# Key Features

- Multi-agent incident investigation
- Automated root cause analysis
- LLM-powered reasoning
- External tool integration
- Semantic runbook search
- Human approval workflow
- Automated engineering reports

---

# Objective

Sentinel AI explores how autonomous AI agents can assist Site Reliability Engineering workflows by combining production signals, reasoning models, and operational knowledge.

```
Detect → Investigate → Diagnose → Recommend → Resolve
```
