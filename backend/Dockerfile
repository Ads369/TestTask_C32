# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application code (not needed if using volumes, but kept for completeness)
# COPY ./app /app/app

# Expose the port
EXPOSE 8000

# Run the app within the virtual environment
# CMD [".venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["fastapi", "run", "app/main.py"]
