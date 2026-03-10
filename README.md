# Meadowa

Meadowa is a Django-based college project.

## Local run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Render deploy

- Push this repository to GitHub.
- Create a Render Web Service from the repo.
- Render can use `render.yaml` automatically.
- Set any extra environment variables you need in Render.

## Important note

The project currently defaults to SQLite. That is acceptable for a simple demo, but production data on Render is better backed by Postgres.
