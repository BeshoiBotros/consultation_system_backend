# Consultation System Backend

Backend for a simple consultation system with JWT auth, patient/consultation CRUD, and AI‑generated summaries using Ollama. The AI summary runs asynchronously via Celery(Background Task).

**What’s inside**
- Django + Django REST Framework
- PostgreSQL for data
- Redis + Celery for background jobs
- Ollama for local LLM inference

**Quickstart (Docker)**
1. `docker compose up --build`
2. Pull the model once: `docker compose exec ollama ollama pull llama3.2:1b`
3. (Optional) create admin: `docker compose exec web python manage.py createsuperuser`
4. API: `http://0.0.0.0:8000/`

**Local dev (without Docker)**
1. Create a virtualenv and install deps: `pip install -r requirements.txt`
2. Create `consultation_system_backend/.env` (see environment variables below)
3. Run Postgres, Redis, and Ollama locally
4. Migrate + run the server:
   - `python manage.py migrate`
   - `python manage.py runserver`
5. Run Celery worker:
   - `celery -A consultation_system_backend worker -l info`
6. Pull the model: `ollama pull llama3.2:1b`

**Environment variables**
These live in `consultation_system_backend/.env`.
- `SECRET_KEY`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` (used by Docker `db`)
- `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`
- `ALLOWED_HOSTS` (comma‑separated)
- `OLLAMA_HOST` (Docker compose sets it to `http://localhost:11434`)

**API routes**
- `POST /accounts/login/` – JWT login
- `POST /accounts/refresh/` – refresh token
- `GET /patients/` – list patients
- `POST /patients/` – create patient
- `PATCH /patients/{uuid}/` – update any patient
- `GET /patients/{uuid}/` – retrieve patient
- `GET /consultations/` – list consultations
- `POST /consultations/` – create consultation
- `POST /consultations/generate-summary/{uuid}/` – enqueue AI summary
- `GET  /consultations/{uuid}/summary_status/` – see the AI summary status for pooling in frontend every 3s
- `PATCH /consultations/{uuid}/` – update any consultations


All protected routes require `Authorization: Bearer <token>`.
