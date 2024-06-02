import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

class QueryClassifier:
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'model.pkl')
    tfidf_vectorizer = None
    model = None

    @classmethod
    def load_model(cls):
        if cls.tfidf_vectorizer is None or cls.model is None:
            model_path = os.path.abspath(cls.model_path)
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            with open(model_path, 'rb') as f:
                cls.tfidf_vectorizer, cls.model = pickle.load(f)

    @classmethod
    def classify_query(cls, messages):
        try:
            cls.load_model()
            user_query = messages[-1]['content']
            user_query_tfidf = cls.tfidf_vectorizer.transform([user_query])
            predicted_values = cls.model.predict(user_query_tfidf)
            
            agentic_probability = predicted_values[0][1]
            
            if agentic_probability > 0.5:
                response = {
                    'model': 'gpt-4-turbo',
                    'score': agentic_probability,
                    'messages': messages
                }
            else:
                response = {
                    'model': 'gpt-3.5-turbo',
                    'score': agentic_probability,
                    'messages': messages
                }
            return response
        except Exception as e:
            print(f"Error classifying query: {str(e)}")
            return None
