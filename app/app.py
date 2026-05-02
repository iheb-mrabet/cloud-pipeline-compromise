from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "message": "Cloud Pipeline Compromise Lab",
        "status": "running"
    }

@app.route("/secret")
def secret():
    try:
        with open("/etc/secrets/API_SECRET", "r") as f:
            secret = f.read().strip()
    except:
        secret = "NOT_FOUND"

    return {"secret": secret}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
