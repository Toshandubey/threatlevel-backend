import pickle

try:
    with open('final_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully:", type(model))
except Exception as e:
    import traceback
    traceback.print_exc()

try:
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    print("Vectorizer loaded successfully:", type(vectorizer))
except Exception as e:
    import traceback
    traceback.print_exc()
