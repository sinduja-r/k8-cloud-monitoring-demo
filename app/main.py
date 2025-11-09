from flask import Flask, jsonify
import os, time

app = Flask(__name__)
BOOT_DELAY = int(os.getenv("READY_DELAY_SECONDS", "5"))
START_TIME = time.time()

@app.get("/")
def home():
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

