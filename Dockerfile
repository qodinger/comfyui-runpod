# Dockerfile for ComfyUI RunPod Serverless
# This containerizes ComfyUI for RunPod serverless deployment

FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install RunPod SDK
RUN pip install --no-cache-dir runpod requests

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p models/checkpoints \
    models/loras \
    models/vae \
    models/clip \
    models/controlnet \
    models/upscale_models \
    output \
    input \
    user

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV COMFYUI_URL=http://localhost:8188
ENV GENERATION_TIMEOUT=300
ENV POLL_INTERVAL=1.0

# Expose port (if needed for debugging)
EXPOSE 8188

# Health check (optional)
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8188/system_stats || exit 1

# Copy startup script
COPY start_serverless.sh /app/start_serverless.sh
RUN chmod +x /app/start_serverless.sh

# Use startup script
CMD ["/app/start_serverless.sh"]

