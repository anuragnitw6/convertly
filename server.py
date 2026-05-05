from flask import Flask, Response
import subprocess

app = Flask(__name__)

# ✅ Serve ads.txt properly
@app.route("/ads.txt")
def ads():
    return Response(
        "google.com, pub-4586891706711357, DIRECT, f08c47fec0942fa0",
        mimetype="text/plain"
    )

# ✅ Run Streamlit app
@app.route("/")
def run_streamlit():
    return subprocess.Popen([
        "streamlit",
        "run",
        "app.py",
        "--server.port", "10000",
        "--server.address", "0.0.0.0"
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
