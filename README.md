# Bakhteyar-AI — Balochi Language Tools

AI tools for the Balochi language: English→Balochi translation and Balochi
text-to-speech, in both Latin and Arabic script.

The repository contains two ways to run the app:

- **`frontend/` + `backend/`** — a modern full-stack rebuild (Next.js +
  TypeScript + Tailwind CSS frontend, Django REST Framework backend).
- **`app.py` + `pages/`** — the original Streamlit app (kept intact).

## Full-Stack App (Next.js + Django)

```
frontend/   Next.js (App Router) + TypeScript + Tailwind CSS
backend/    Django REST Framework API (/api/translate/, /api/tts/)
```

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py runserver
```

The API runs at `http://127.0.0.1:8000` with:

- `POST /api/translate/` — `{ "text", "script" }` → Balochi translation
- `POST /api/tts/` — `{ "text", "script" }` → base64 WAV audio
- `GET /api/health/` — health check

`script` is `"latin"` or `"arabic"`.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local   # optional; defaults to http://127.0.0.1:8000
npm run dev
```

Open `http://localhost:3000`. Next.js proxies `/api/*` to the Django backend
(see `frontend/next.config.ts`), so run the backend alongside it.

## Original Streamlit App

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy On Streamlit Community Cloud

1. Create a GitHub repository.
2. Add `app.py` and `requirements.txt`.
3. Go to Streamlit Community Cloud.
4. Select the repository.
5. Set the main file path to:

```text
app.py
```

6. Deploy the app.
