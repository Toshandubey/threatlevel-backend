import os
import imaplib
import email
from email.header import decode_header
import joblib
import pandas as pd
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load env variables
load_dotenv()

app = Flask(__name__)
# Allow CORS for all origins for testing/Vercel
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'final_model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')

# Global variables for caching the model
model = None
vectorizer = None
model_error = "Not loaded yet"

def load_models():
    global model, vectorizer, model_error
    if model is None or vectorizer is None:
        try:
            model = joblib.load(MODEL_PATH)
        except Exception as e:
            model_error = f"Model err: {str(e)}"
            return

        try:
            vectorizer = joblib.load(VECTORIZER_PATH)
        except Exception as e:
            model_error = f"Vectorizer err: {str(e)}"

def get_text_from_email(msg):
    text = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            # We want plain text if available
            if content_type == "text/plain":
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        text += payload.decode(errors='ignore')
                except Exception:
                    pass
    else:
        content_type = msg.get_content_type()
        if content_type == "text/plain" or content_type == "text/html":
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    text += payload.decode(errors='ignore')
            except Exception:
                pass
    return text.strip()

@app.route('/', methods=['GET'])
def serve_frontend():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/scan_inbox', methods=['GET', 'POST', 'OPTIONS'])
def scan_inbox():
    load_models()
    
    username = None
    password = None

    if request.method == 'POST' and request.is_json:
        data = request.get_json()
        username = data.get("email")
        password = data.get("password")

    if not username or not password:
        username = os.environ.get("IMAP_EMAIL")
        password = os.environ.get("IMAP_PASSWORD")

    if not username or not password:
        return jsonify({"error": "No credentials provided. Please supply an email and App Password."}), 400

    try:
        # connect to host using SSL
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        if status != "OK":
            return jsonify({"error": "Could not fetch emails"}), 500
        
        email_ids = messages[0].split()
        # get last 5 emails
        latest_email_ids = email_ids[-5:]
        
        results = []
        
        for e_id in reversed(latest_email_ids):
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # decode email subject
                    subject, encoding = decode_header(msg.get("Subject", ""))[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8", errors='ignore')
                        
                    # decode email sender
                    sender, encoding = decode_header(msg.get("From", ""))[0]
                    if isinstance(sender, bytes):
                        sender = sender.decode(encoding if encoding else "utf-8", errors='ignore')
                        
                    # get the body content
                    text_content = get_text_from_email(msg)
                    
                    prediction = "unknown"
                    if not model or not vectorizer:
                        prediction = f"Model load failed: {model_error} at path {MODEL_PATH}"
                    elif text_content:
                        try:
                            # If vectorizer expects iterables
                            text_vec = vectorizer.transform([text_content])
                            pred = model.predict(text_vec)
                            prediction_val = pred[0]
                            
                            if str(prediction_val) == '1':
                                prediction = "phishing"
                            elif str(prediction_val) == '0':
                                prediction = "clean"
                            else:
                                prediction = str(prediction_val)
                        except Exception as e:
                            print("Prediction error:", e)
                            prediction = f"error: {str(e)}"
                    
                    results.append({
                        "subject": subject,
                        "sender": sender,
                        "snippet": text_content[:250] + "..." if len(text_content) > 250 else text_content,
                        "prediction": prediction
                    })
        mail.logout()
        return jsonify({"data": results}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Bind to PORT strictly defined by environments like Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
