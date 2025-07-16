# Base image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-extra \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables (override in production)
ENV IBMQ_TOKEN="your_ibmq_token"
ENV OPENAI_API_KEY="your_openai_key"
ENV PORT=8000

# Expose API port
EXPOSE $PORT

# Command to run the application
CMD ["uvicorn", "qmetagpt.frontend_interface.app:app", "--host", "0.0.0.0", "--port", "$PORT"]