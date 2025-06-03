- / (CV list) loads
- /cv/1/ (CV detail) loads
- /cv/1/pdf/ generates a PDF
- /cv/1/email/ sends email via celery
- /api/cvs/ shows the DRF browsable API
- /logs/ shows recent requests (no errors)
- /settings/ displays your settings (DEBUG, ALLOWED_HOSTS, etc.)

Running instance:
- Remove any old containers & anonymous volumes - docker compose down --volumes
- Build fresh images and start both services - docker compose up --build

- For OpenAI translation - fill YOUR_OPENAI_API_KEY
