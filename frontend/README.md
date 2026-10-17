# Incident Agent Frontend

React + Vite UI for the local AI Production Incident Resolution Agent.

## Requirements
- Node.js 20+ (LTS recommended)
- Spring Boot backend running on `http://localhost:8081`
- AI service running on `http://localhost:8000`
- Ollama running on `http://localhost:11434` with the configured model pulled
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
- `POST /ai-api/investigate/{id}` (proxied by Vite to the AI service)

The AI service can be started from the repository root with:

```powershell
cd ai-service
python -m uvicorn app.main:app --reload --port 8000
```

The AI service calls Ollama and Spring Boot using `OLLAMA_BASE_URL`, `OLLAMA_MODEL`,
and `BACKEND_BASE_URL` from its environment (defaults: `localhost:11434`,
`qwen2.5:7b`, and `localhost:8081`). Ensure Ollama has the model available before
running an investigation.

## If the browser reports a CORS error
The backend must allow the Vite development origin. The simplest local-only option is to add `@CrossOrigin(origins = "http://localhost:5173")` to `IncidentController` and `InvestigationController`, then restart Spring Boot. If your controller classes differ, use the same annotation on the controllers that serve these endpoints.

The AI investigation request uses Vite's development proxy, so browser CORS does
not need to be enabled on the AI service.
