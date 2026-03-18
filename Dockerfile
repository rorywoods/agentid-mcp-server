FROM python:3.12-slim


# Disable buffering for std/stout
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
# Use --noc-cache-dir to reduce image size by not storing pip cache
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app

EXPOSE 8080

CMD ["python", "server.py"]