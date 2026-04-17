import os
import joblib
from pprint import pprint
import base64
from flask import Flask, jsonify, send_from_directory, request, redirect, session, url_for
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import google_auth_oauthlib.flow

load_dotenv()

app = Flask(__name__)
# Secret key for session management (required for OAuth)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-key-123")
CORS(app, supports_credentials=True)

# Database Setup (SQLite for local, could be Postgres in prod)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    token = db.Column(db.String(1000), nullable=False)
    refresh_token = db.Column(db.String(1000))
    token_uri = db.Column(db.String(500))
    client_id = db.Column(db.String(500))
    client_secret = db.Column(db.String(500))
    scopes = db.Column(db.String(1000))

# Initialize DB
with app.app_context():
    db.create_all()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'final_model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')

CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "client_secrets.json")

# Note: Using the exact scope required for Gmail Readonly
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/userinfo.email', 'openid']

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
        try:
            vectorizer = joblib.load(VECTORIZER_PATH)
        except Exception as e:
            model_error = f"Vectorizer err: {str(e)}"

@app.route('/', methods=['GET'])
def serve_frontend():
    return send_from_directory(BASE_DIR, 'index.html')

# ==========================================
# OAUTH 2.0 ROUTES
# ==========================================

@app.route('/login/google')
def login_google():
    # Allow insecure HTTP OAuth testing for localhost
    if "localhost" in request.url_root or "127.0.0.1" in request.url_root:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    
    # Dynamically point back to the host we came from
    flow.redirect_uri = request.url_root.rstrip('/') + url_for('auth_callback')

    # Generate URL for request to Google's OAuth 2.0 server.
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent' # Force consent to always get a refresh token
    )

    # Store state so the callback can verify the auth server response.
    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def auth_callback():
    if "localhost" in request.url_root or "127.0.0.1" in request.url_root:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        
    state = session.get('state')
    
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = request.url_root.rstrip('/') + url_for('auth_callback')

    # Provide Google the auth response to get access tokens
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    
    credentials = flow.credentials
    
    # Get user email
    service = build('oauth2', 'v2', credentials=credentials)
    user_info = service.userinfo().get().execute()
    email = user_info['email']
    
    # Store in DB
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        db.session.add(user)
        
    user.token = credentials.token
    # Google sometimes doesn't send a refresh token if already granted, so keep the old one if it exists
    if credentials.refresh_token:
        user.refresh_token = credentials.refresh_token
        
    user.token_uri = credentials.token_uri
    user.client_id = credentials.client_id
    user.client_secret = credentials.client_secret
    user.scopes = ",".join(credentials.scopes) if credentials.scopes else ""
    
    db.session.commit()
    
    # Start session
    session['user_email'] = email
    
    # Redirect back to the single-page app
    return redirect('/')

@app.route('/auth_status', methods=['GET'])
def auth_status():
    if 'user_email' in session:
        return jsonify({"authenticated": True, "email": session['user_email']})
    return jsonify({"authenticated": False})
    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_email', None)
    return jsonify({"success": True})

# ==========================================
# SCAN API
# ==========================================

@app.route('/scan_inbox', methods=['GET', 'POST', 'OPTIONS'])
def scan_inbox():
    load_models()
    
    if 'user_email' not in session:
        return jsonify({"error": "Unauthorized. Please Sign in with Google first."}), 401
        
    user = User.query.filter_by(email=session['user_email']).first()
    if not user:
        return jsonify({"error": "User missing from DB."}), 404
        
    try:
        # Reconstruct OAuth Credentials object from DB
        creds = Credentials(
            token=user.token,
            refresh_token=user.refresh_token,
            token_uri=user.token_uri,
            client_id=user.client_id,
            client_secret=user.client_secret,
            scopes=user.scopes.split(',') if user.scopes else SCOPES
        )
        
        # Connect to Gmail API
        service = build('gmail', 'v1', credentials=creds)
        
        # Get latest 5 emails from Inbox
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=5).execute()
        messages = results.get('messages', [])
        
        scan_results = []
        
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            
            payload = msg_data.get('payload', {})
            headers = payload.get('headers', [])
            
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
            sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown Sender")
            snippet = msg_data.get('snippet', '')
            
            # Extract plain text for ML model
            body_text = ""
            if 'parts' in payload:
                for part in payload['parts']:
                    if part.get('mimeType') == 'text/plain':
                        data = part.get('body', {}).get('data', '')
                        if data:
                            body_text = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            else:
                data = payload.get('body', {}).get('data', '')
                if data:
                    body_text = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    
            text_content = body_text.strip() if body_text else snippet
            
            prediction = "unknown"
            if not model or not vectorizer:
                prediction = "Model error"
            elif text_content:
                try:
                    text_vec = vectorizer.transform([text_content])
                    pred = model.predict(text_vec)
                    prediction_val = pred[0]
                    prediction = "phishing" if str(prediction_val) == '1' else "clean"
                except Exception as e:
                    prediction = f"err: {str(e)}"
            
            scan_results.append({
                "subject": subject,
                "sender": sender,
                "snippet": text_content[:250] + "..." if len(text_content) > 250 else text_content,
                "prediction": prediction
            })
            
        return jsonify({"data": scan_results}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
