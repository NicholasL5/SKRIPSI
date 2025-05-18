from flask import Flask, render_template, request, jsonify, session, make_response
import requests, os, json
from Helpers.convert import clean_latex
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ENDPOINT = os.getenv("MODEL_API")
HF_TOKEN = os.getenv("HF_TOKEN")
headers  = {"Authorization": f"Bearer {HF_TOKEN}"}
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-only-fallback")


def build_response(message="success", status="success", data=None, status_code=200):
    payload = {
        "status": status,
        "message": message
    }
    
    if data is not None:
        payload["data"] = data

    return make_response(jsonify(payload), status_code)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]

    history = session.get("history", [])
    history.append({"role": "user", "content": msg})

    payload = {
        "inputs": history
    }

    try:
        r = requests.post(ENDPOINT, headers=headers, json=payload, timeout=120)
        r.raise_for_status()
    except Exception as e:
        return build_response(message=str(e), status="error", status_code=500)

    answer = r.json()[0]["generated_text"]

    history.append({"role": "assistant", "content": answer})
    session["history"] = history
    cleaned_answer = clean_latex(answer)
    return build_response(
        message="success",
        status="success",
        data={"reply": cleaned_answer},
        status_code=200
    )

@app.route("/delete-history", methods=["DELETE"])
def clear_history():
    session.pop("history", None)
    return build_response(
        message="History cleared",
        status="success",
        status_code=200
    )

@app.route("/regenerate", methods=["DELETE"])
def pop_last_conversation():
    history = session.get("history", [])
    if len(history) >= 2:
        history.pop()
        history.pop()
        session["history"] = history

        return build_response(
            message="Last conversation turn removed",
            status="success",
            status_code=200
        )
    else:
        return build_response(
            message="Nothing to regenerate",
            status="error",
            status_code=400
        )

if __name__ == "__main__":

    app.run(debug=True)