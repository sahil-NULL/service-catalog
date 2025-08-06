
#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies if requirements.txt is newer than last install
if [ requirements.txt -nt venv/pyvenv.cfg ]; then
    echo "Installing/updating dependencies..."
    pip install -r requirements.txt
fi

# Note: Skipping database migrations for now due to import path issues
# TODO: Fix alembic configuration for proper database migrations
echo "Note: Database migrations skipped. The app will create tables automatically."

# Start the FastAPI server
echo "Starting FastAPI server..."
uvicorn server.main:app --reload --host 0.0.0.0 --port 8000 