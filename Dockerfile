FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install once
COPY requirements.txt .
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Run both FastAPI and Streamlit
CMD ["bash", "-c", "uvicorn api.main:app --host 0.0.0.0 --port 8000 & streamlit run app/main.py --server.port=7860 --server.address=0.0.0.0"]
