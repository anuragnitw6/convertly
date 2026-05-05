from flask import Flask, send_file
import subprocess
import threading

app = Flask(__name__)

# 🔥 Serve ads.txt properly
@app.route('/ads.txt')
def ads():
    return send_file('ads.txt', mimetype='text/plain')

# 🔥 Run Streamlit in background
def run_streamlit():
    subprocess.run([
        "streamlit",
        "run",
        "app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])

threading.Thread(target=run_streamlit).start()

# 🔥 Redirect root to Streamlit
@app.route('/')
def index():
    return "Streamlit app running..."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
