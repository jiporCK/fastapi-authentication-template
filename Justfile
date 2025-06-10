# 🐍 Set up Python virtual environment
vmpy:
    python3 -m venv venv
    echo "Virtual environment created in ./venv"

# 🚀 Run the FastAPI app with Uvicorn
run:
    # source venv/bin/activate
    uvicorn app.main:app --reload

push:
    git add .
    git commit -m "default commit"
    git push
