from flask import Flask, jsonify, Response
import os, time
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST


app = Flask(__name__)
BOOT_DELAY = int(os.getenv("READY_DELAY_SECONDS", "5"))
START_TIME = time.time()

PAGE_HITS = Counter(
    "flask_homepage_requests_total",
    "Total Number of Homepage requests",
    ["method"]
)

@app.get("/")
def home():
    PAGE_HITS.labels(method="GET").inc()
    msg = os.getenv("APP_MESSAGE", "Hello from Kubernetes!")
    return jsonify(message=msg), 200

@app.get("/health")
def health():
    return "ok", 200

@app.get("/ready")
def ready():
    if time.time() - START_TIME < BOOT_DELAY:
        return "not ready", 503
    return "ready", 200

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

