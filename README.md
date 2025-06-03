- / (CV list) loads
- /cv/1/ (CV detail) loads
- /cv/1/pdf/ generates a PDF
- /cv/1/email/ sends email via celery
- /api/cvs/ shows the DRF browsable API
- /logs/ shows recent requests (no errors)
- /settings/ displays your settings (DEBUG, ALLOWED_HOSTS, etc.)

- Starting server - python3 manage.py runserver
- Loading Initial Data - python3 manage.py loaddata initial_cvs.json
- Running Tests - python3 manage.py test

- Remove any old containers & anonymous volumes - docker compose down --volumes
- Build fresh images and start both services in the background - docker compose up -d --build

- For OpenAI translation - fill YOUR_OPENAI_API_KEY
