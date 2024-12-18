FROM nvidia/cuda:11.6.2-base-ubuntu20.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY model_server.py .

CMD ["python3", "model_server.py"]