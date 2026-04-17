import requests
import base64
import zlib

# The exact mermaid code for your diagram
mermaid_code = """flowchart TD
    classDef frontend fill:#1e1e2e,stroke:#77dc7a,stroke-width:2px,color:#fff;
    classDef backend fill:#11111b,stroke:#89b4fa,stroke-width:2px,color:#fff;
    classDef database fill:#181825,stroke:#f38ba8,stroke-width:2px,color:#fff;
    classDef google fill:#ffffff,stroke:#4285F4,stroke-width:2px,color:#000;
    classDef mlcore fill:#313244,stroke:#f9e2af,stroke-width:2px,color:#fff;
    classDef threat fill:#313244,stroke:#990000,stroke-width:3px,color:#fff;

    client(Frontend Single Page Application):::frontend
    oauth(Google OAuth 2.0 Auth):::google
    db[(SQLite User Database)]:::database
    server(Flask Cloud Backend):::backend
    gmail(Gmail Read API):::google
    vectorizer([Tf-Idf Vectorizer Layer]):::mlcore
    model([Random Forest Classifier Matrix]):::mlcore
    phishing{Threat Detected?}:::threat
    
    subgraph "Phase 1: Zero-Trust Authentication"
        client -- 1. Clicks 'Sign in with Google' --> oauth
        oauth -- 2. Approves Read-Only Scopes --> server
        server -- 3. Encrypts & Stores Key --> db
        server -- 4. Grants Secure Session --> client
    end
    
    subgraph "Phase 2: Target Data Extraction"
        client -- 5. Signals New Scan --> server
        server -- 6. Pulls Valid Key --> db
        server -- 7. Dispatches API Request --> gmail
        gmail -- 8. Ingress 5 Recent Payloads --> server
    end
    
    subgraph "Phase 3: Deep Neural Inference"
        server -- 9. Strips HTML & Injects Plaintext --> vectorizer
        vectorizer -- 10. Transforms Strings to Arrays --> model
        model -- 11. Generates Threat Probability --> phishing
        phishing -- "Class 1: Spear Phishing" --> server
        phishing -- "Class 0: Clean Transmission" --> server
    end
    
    server -- 12. Returns JSON Forensics --> client
"""

print("Compressing diagram data...")
# Compressing the string via zlib (Kroki API requirement)
compressed = zlib.compress(mermaid_code.encode('utf-8'))
encoded = base64.urlsafe_b64encode(compressed).decode('ascii')

# We request a transparent PNG 
# We request dark mode 
url = f"https://kroki.io/mermaid/png/{encoded}"

print(f"Requesting generated image from Kroki...")
response = requests.get(url)

if response.status_code == 200:
    with open("architecture_diagram.png", "wb") as f:
        f.write(response.content)
    print("Success! Downloaded as 'architecture_diagram.png'.")
else:
    print(f"Error {response.status_code}: {response.text}")
