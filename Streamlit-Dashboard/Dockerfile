# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
COPY .streamlit/secrets.toml .streamlit/secrets.toml

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all other files
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the app
CMD ["streamlit", "run", "0_🏠_HOME.py", "--server.port=8501", "--server.address=0.0.0.0"]