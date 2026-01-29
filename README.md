# AI Worker Productivity Dashboard (MLOps Project)

A full-stack MLOps dashboard that simulates factory worker events and visualizes real-time operational and business KPIs using FastAPI, PostgreSQL, and an interactive web UI.

Live Dashboard  
👉 https://mlops-worker-dashboard-824d447cfb96.herokuapp.com  

Health Check  
👉 https://mlops-worker-dashboard-824d447cfb96.herokuapp.com/api/health  

API Docs (Swagger)  
👉 https://mlops-worker-dashboard-824d447cfb96.herokuapp.com/docs  


## Features

### Business KPIs
- Throughput (units/hour)
- Production Rate
- Yield (units/event)
- Idle Ratio (%)
- Average Utilization (%)
- Bottleneck Worker Detection

### Operational Metrics
- MTBF (Mean Time Between Failures)
- MTTR (Mean Time To Recovery)
- Total Active Time (minutes)
- Total Idle Time (minutes)

### Analytics & Visualization
- Events over time (time-series)
- Products over time
- Worker productivity comparison
- Active vs Idle distribution
- Filter by time window and worker

### Platform Capabilities
- REST APIs using FastAPI
- PostgreSQL database on Heroku
- Health endpoint for monitoring
- Auto-generated API documentation
- Fully deployed production app

## Architecture

Browser (HTML + JS + Chart.js)
        ↓
FastAPI Backend
        ↓
SQLAlchemy ORM
        ↓
PostgreSQL (Heroku)


Data simulation generates worker events which are persisted and analyzed dynamically.


## Tech Stack

- Backend: Python, FastAPI
- Database: PostgreSQL (Heroku), SQLite (local)
- ORM: SQLAlchemy
- Frontend: HTML, CSS, JavaScript, Chart.js
- Deployment: Heroku
- Version Control: GitHub

---

## API Endpoints

| Endpoint | Description |
|------------|-------------|
| `/api/health` | Service health check |
| `/api/metrics/summary` | Summary KPIs |
| `/api/metrics/analytics` | Business + Operational KPIs |
| `/api/metrics/workers` | Worker-level metrics |
| `/api/metrics/workstations` | Workstation metrics |
| `/api/metrics/timeseries` | Time-series analytics |

Interactive documentation available at `/docs`.


## Local Setup

```bash
git clone https://github.com/inafees14/mlops-worker-dashboard.git
cd mlops-worker-dashboard
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open in browser:

```bash
http://127.0.0.1:8000
```

## Deployment

The application is deployed on Heroku using:

- Procfile

- PostgreSQL add-on

- Git-based deployment

- Automatic health monitoring

## Objective

This project demonstrates production-ready MLOps engineering skills including:

- Data simulation and ingestion

- KPI engineering and analytics pipelines

- Monitoring readiness

- Cloud deployment

- Interactive visualization

- API documentation

## Author

Mohammad Nafees Iqbal

M.Sc Data Science

GitHub: https://github.com/inafees14