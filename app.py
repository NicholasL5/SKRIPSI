from flask import Flask, render_template, request, jsonify, session
import requests, os, json
from Helpers.convert import clean_latex
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ENDPOINT = os.getenv("MODEL_API")
HF_TOKEN = os.getenv("HF_TOKEN")
headers  = {"Authorization": f"Bearer {HF_TOKEN}"}
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-only-fallback")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]

    history = session.get("history", [])
    history.append({"role": "user", "content": msg})

    payload = {
        "inputs": history,
        "parameters": {"return_full_text": False}
    }

    try:
        r = requests.post(ENDPOINT, headers=headers, json=payload, timeout=120)
        r.raise_for_status()
    except Exception as e:
        print(f"Request failed: {e}")

    answer = r.json()[0]["generated_text"]

    history.append({"role": "assistant", "content": answer})
    session["history"] = history
    return clean_latex(answer)

@app.route("/delete-history", methods=["DELETE"])
def clear_history():
    session.pop("history", None)             
    return "cleared", 200

@app.route("/regenerate", methods=["DELETE"])
def pop_last_conversation():
    session['history'].pop()
    session['history'].pop()
    return "regenerated", 200

if __name__ == "__main__":

    app.run(debug=True)