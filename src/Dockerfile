FROM python:3.12-slim

WORKDIR /app

COPY . .

COPY env .

RUN ls -R /app

RUN pip install --no-cache-dir -r requirements.txt

# Expose port for FastAPI
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]