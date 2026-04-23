# 1. Use a lightweight Python base image
FROM python:3.10-slim

# 2. Set the working directory
WORKDIR /app

# 3. Copy requirements first
COPY requirements.txt .

# 4. PRO MLOPS TRICK: Install the CPU-only version of PyTorch first!
# This prevents it from downloading the massive 3GB GPU version.
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

# 5. Install the rest of the ML libraries
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy application code
COPY . .

# 7. Expose port and run
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
