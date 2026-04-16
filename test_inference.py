import joblib
import traceback

def test_inference():
    try:
        print("Loading models...")
        model = joblib.load('final_model.pkl')
        vectorizer = joblib.load('vectorizer.pkl')
        print("Models loaded successfully")
        
        test_text = "This is a test email text to predict."
        
        print("Transforming text...")
        text_vec = vectorizer.transform([test_text])
        
        print("Predicting...")
        pred = model.predict(text_vec)
        
        print("Prediction successful:", pred)
    except Exception as e:
        print("FAILED WITH EXCEPTION:")
        traceback.print_exc()

if __name__ == "__main__":
    test_inference()
