aws-agent-wordpress/
│── .venv/           # local virtual environment (✅ don't push to GitHub)
│── __pycache__/     # Python cache files (✅ ignore in GitHub)
│── .env             # contains your GEMINI_API_KEY (❌ don't push, add to .gitignore)
│── .gitignore       # good, make sure it includes .env, .venv, __pycache__
│── .python-version  # optional, for version managers (fine)
│── app.py           # your FastAPI + Agent app (✅ main entry)
│── pyproject.toml   # poetry/pdm metadata (optional, AWS won’t use it)
│── README.md        # keep as project notes
│── requirements.txt # ✅ AWS will use this to install dependencies
│── uv.lock          # can ignore, not needed for AWS


