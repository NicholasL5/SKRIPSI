from flask import Flask, render_template, request, jsonify, session, make_response
import requests, os, json, logging
from Helpers.convert import clean_latex
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModel
import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity

env_loaded = load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

app = Flask(__name__)

# Configuration
ENDPOINT = os.getenv("MODEL_API")
HF_TOKEN = os.getenv("HF_TOKEN")
headers  = {"Authorization": f"Bearer {HF_TOKEN}"}
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-only-fallback")
MAX_TURNS = 10

# Embedding model setup
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
device     = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer  = AutoTokenizer.from_pretrained(EMBED_MODEL)
model      = AutoModel.from_pretrained(EMBED_MODEL).to(device).eval()

@torch.inference_mode()
def _encode(texts):
    tokens = tokenizer(texts, padding=True, truncation=True, return_tensors="pt").to(device)
    outputs = model(**tokens)
    hidden = outputs.last_hidden_state
    mask = tokens.attention_mask.unsqueeze(-1)
    summed = (hidden * mask).sum(dim=1)
    counts = mask.sum(dim=1)
    emb = summed / counts
    emb = torch.nn.functional.normalize(emb, p=2, dim=1)
    return emb.cpu().numpy()

def is_topic_shift(new_msg, history, k=3, threshold=0.70):
    logging.info("Checking for topic shift...")

    if not history:
        logging.info("No history, not a topic shift.")
        return False

    context_texts = []

    last_message = history[-1]
    if last_message["role"] == "assistant":
        context_texts.append(last_message["content"])

    user_msgs = [h["content"] for h in history if h["role"] == "user"]
    context_texts.extend(user_msgs[-k:])

    if not context_texts:
        logging.info("No relevant context to compare against.")
        return False

    embs = _encode([new_msg] + context_texts)
    
    sims = cosine_similarity(embs[0:1], embs[1:])[0]
    
    max_sim = np.max(sims)
    
    logging.info(f"Max similarity with context: {max_sim:.4f} || Threshold: {threshold}")
    
    return float(max_sim) < threshold

def build_response(message="success", status="success", data=None, status_code=200):
    payload = {"status": status, "message": message}
    if data is not None:
        payload["data"] = data
    return make_response(jsonify(payload), status_code)

def pop_last_history():
    history = session.get("history", [])
    if history:
        history.pop()
        session["history"] = history
        logging.info(f"History after pop: {session.get('history')}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    payload = request.get_json()
    msg = payload.get("msg", "")
    history = session.get("history", [])

    logging.info(f"Session before chat: {history}")
    shift = is_topic_shift(msg, history)
    shift = False
    if shift:
        logging.info("Topic shift detected, resetting context to last user message")
        session["history"] = [{"role": "user", "content": msg}]
        return build_response(
            message="success", status="success", data={"reply": "SHIFTING"}, status_code=200
        )
    else:
        history.append({"role": "user", "content": msg})
        session["history"] = history[-MAX_TURNS:]
    logging.info(f"Session to send to model: {session.get('history')}")


    request_payload = {"inputs": session["history"]}
    try:
        r = requests.post(ENDPOINT, headers=headers, json=request_payload, timeout=120)
        r.raise_for_status()
    except requests.exceptions.HTTPError as ehttp:
        status = ehttp.response.status_code
        logging.error(f"HTTPError {status}: {ehttp.response.text}")
        if status == 400:
            pop_last_history()
            return build_response(
                message="Service sedang mati atau tidak tersedia. Mohon maaf atas ketidaknyamananya.",
                status="fail", status_code=400
            )
    except Exception as e:
        pop_last_history()
        logging.exception("Error while calling model API")
        return build_response(message=str(e), status="error", status_code=500)

    # Process successful response
    answer = r.json()[0].get("generated_text", "")

    session["history"].append({"role": "assistant", "content": answer})
    logging.info(f"Session after response: {session.get('history')}")
    cleaned_answer = clean_latex(answer)
    return build_response(
        message="success", status="success", data={"reply": cleaned_answer}, status_code=200
    )

@app.route("/delete-history", methods=["DELETE"])
def clear_history():
    session.pop("history", None)
    logging.info("Session cleared")
    return build_response(
        message="History cleared", status="success", status_code=200
    )

@app.route("/regenerate", methods=["DELETE"])
def pop_last_conversation():
    history = session.get("history", [])
    logging.info(f"Session before regenerate pop: {history}")

    if len(history) >= 2:
        history.pop()
        history.pop()
        session["history"] = history
        logging.info(f"Session after regenerate pop: {session.get('history')}")
        return build_response(
            message="Last conversation turn removed", status="success", status_code=200
        )
    else:
        logging.warning("Nothing to regenerate in session")
        return build_response(
            message="Nothing to regenerate", status="error", status_code=400
        )




if __name__ == "__main__":
    logging.info("Starting Flask app")
    fh = logging.FileHandler('app.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    logging.getLogger().addHandler(fh)
    app.run()