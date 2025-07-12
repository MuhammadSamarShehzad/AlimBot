FROM python:3.10-slim

WORKDIR /app

# Copy only requirements first to cache dependencies
COPY ../requirements.txt .

RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Now copy the rest of your app code
COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
