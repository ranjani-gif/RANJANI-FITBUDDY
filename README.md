# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI + Jinja2 + SQLite application that uses Google's Gemini API to generate a 7-day general-wellness workout plan, a nutrition/recovery tip, and an AI-updated plan from user feedback.

## Project structure

```text
FitBuddy/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── gemini_client.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   ├── updated_plan.py
│   └── routes.py
├── templates/
│   ├── index.html
│   ├── result.html
│   └── all_users.html
├── static/
│   └── style.css
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 1. Open in VS Code

Open the `FitBuddy` folder in VS Code.

## 2. Create a virtual environment

### Windows PowerShell

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```bat
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Gemini

Copy `.env.example` to `.env`:

```text
GOOGLE_API_KEY=your_real_key
GEMINI_WORKOUT_MODEL=gemini-2.5-flash
GEMINI_TIP_MODEL=gemini-2.5-flash
ADMIN_KEY=choose-a-long-secret
```

Never commit `.env` to Git.

If the model names are unavailable for your Gemini API key, replace them with model names supported by your account.

## 5. Start the application

From the FitBuddy folder:

```bash
uvicorn app.main:app --reload
```

Open:

- Website: http://127.0.0.1:8000
- FastAPI docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/api/health
- Admin dashboard: http://127.0.0.1:8000/view-all-users?key=YOUR_ADMIN_KEY

## 6. Test the main flow

1. Open the home page.
2. Enter a test name and unique User ID.
3. Enter age, weight, goal, and intensity.
4. Click **Generate Plan**.
5. Confirm that a 7-day plan and nutrition/recovery tip appear.
6. Enter feedback such as `Add more flexibility and recovery activities`.
7. Click **Update with AI**.
8. Open the admin dashboard using your `ADMIN_KEY`.
9. Confirm the user is listed.
10. Confirm the updated plan is retained.

## API endpoints

### `GET /`
Shows the input form.

### `POST /generate-workout`
Creates/updates the user, calls Gemini for the workout plan and tip, and stores the result.

### `POST /submit-feedback`
Gets the user's latest plan, sends the original plan plus feedback to Gemini, and stores the revised plan.

### `GET /view-all-users?key=...`
Admin dashboard.

### `POST /delete-user`
Deletes a user and their stored plans after admin-key validation.

### `GET /api/health`
Returns a simple health response.

### `GET /api/users?key=...`
Returns user records as JSON after admin-key validation.

## Troubleshooting

### `GOOGLE_API_KEY is not configured`
Create `.env` in the project root and add your API key.

### Model not found / permission error
Set `GEMINI_WORKOUT_MODEL` and `GEMINI_TIP_MODEL` to models currently available to your Gemini API key.

### Template/static errors
Run Uvicorn from the project root, the directory containing `app`, `templates`, and `static`.

### Database
SQLite database `fitbuddy.db` is created automatically on first start. It is ignored by Git.

## Important note

This project is based on the supplied FitBuddy documentation. The documentation names older Gemini 1.5 Pro/Flash models and the older `google-generativeai` package. This implementation keeps the same architecture and features but uses the current-style `google-genai` client and configurable model names so the app can be adapted when model availability changes.

The generated fitness content is intentionally framed as general wellness information and does not provide medical diagnosis or extreme diet/exercise instructions.
