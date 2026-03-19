# Webapp

Simple Flask app (run calculator) — prepared for deployment.

Quick start (local):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask run --host=0.0.0.0 --port=5000
```

Docker (build and run):

```bash
docker build -t webapp:local .
docker run -p 5000:5000 webapp:local
```

Deployment notes:
- Add a GitHub repo and push this folder (`webapp/`).
- On Render, create a new Web Service and connect the repo; set the build command to `pip install -r requirements.txt` and start command to `gunicorn "webapp.app:app" --bind 0.0.0.0:$PORT`.
- For GitHub Actions-based deploys, add the provider-specific secrets (e.g., `RENDER_API_KEY`, `RENDER_SERVICE_ID`).
