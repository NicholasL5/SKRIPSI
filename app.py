from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
import torch
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

hf_token = os.environ.get("HF_TOKEN")
if hf_token:
    login(hf_token)
else:
    print("Warning: HF_TOKEN not found in environment variables. Authentication might fail.")

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")
model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2")

app = Flask(__name__)

session_histories = {}

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        msg = request.form["msg"]
        session_id = request.cookies.get('session_id', 'default')
        response = get_chat_response(msg, session_id)
        return response
    return "Method not allowed", 405

def get_chat_response(text, session_id='default'):
    chat_history_ids = session_histories.get(session_id, None)
    
    new_user_input_ids = tokenizer.encode(
        str(text) + tokenizer.eos_token, 
        return_tensors='pt'
    )
    
    if chat_history_ids is not None:
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
    else:
        bot_input_ids = new_user_input_ids
    
    # Generate response
    with torch.no_grad():
        chat_history_ids = model.generate(
            bot_input_ids, 
            max_length=bot_input_ids.shape[-1] + 100,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.5,
            top_p=0.9
        )
    
    session_histories[session_id] = chat_history_ids
    
    response = tokenizer.decode(
        chat_history_ids[:, bot_input_ids.shape[-1]:][0], 
        skip_special_tokens=True
    )
    
    return response

if __name__ == '__main__':
    app.run(debug=True)