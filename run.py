# run.py
from dotenv import load_dotenv

# Load .env before anything else
load_dotenv()

from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug=True enables hot-reload and detailed errors
    app.run(debug=True)
