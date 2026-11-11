# Incident Agent Frontend

React + Vite UI for the local AI Production Incident Resolution Agent.

## Requirements
- Node.js 20+ (LTS recommended)
- Spring Boot backend running on `http://localhost:8081`
- The hosted AI service at `https://ai-powered-production-incident-yja8.onrender.com` for the Run investigation button
- Synthetic incident data seeded into the backend

## Run it
Open PowerShell in this folder:

```powershell
npm install
npm run dev
```

Open the URL Vite prints, usually `http://localhost:5173`.

## API endpoints used
- `GET http://localhost:8081/api/incidents`
- `GET http://localhost:8081/api/incidents/{id}/investigation-data`
- `POST https://ai-powered-production-incident-yja8.onrender.com/investigate/{id}` (AI investigation button only)

For local AI service development, start it from the repository root with:

```powershell
cd ai-service
python -m uvicorn app.main:app --reload --port 8000
```

The AI service calls its configured LLM provider and Spring Boot using its
environment settings. The hosted service must have a reachable backend configured
with `BACKEND_BASE_URL`.

## If the browser reports a CORS error
Spring Boot must allow the Vite development origin for incident and evidence
requests. The AI service must allow the frontend origin for the Run investigation
request; `ai-service/app/main.py` allows both local Vite and the deployed Vercel
frontend.
