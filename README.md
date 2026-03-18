## Starhub Monorepo

This repository contains:

- `frontend/`: uni-app + Vue 3 frontend
- `backend/`: FastAPI + PostgreSQL backend (MVP)

## Backend (Docker Compose)

### Start

```bash
cp .env.example .env
# Edit .env and change POSTGRES_PASSWORD
docker compose up -d --build
```

### Verify

```bash
curl http://localhost:8000/health
```

Open API docs:

- `http://localhost:8000/docs`

## Only download backend code (sparse checkout)

If you only need backend + compose files on another machine:

```bash
git clone --filter=blob:none --no-checkout <REPO_URL> starhub
cd starhub
git sparse-checkout init --cone
git sparse-checkout set backend docker-compose.yml .env.example README.md
git checkout main
```

