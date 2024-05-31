import pandas as pd
import os
from joblib import load
from sentiment_model.config.core import fetch_config_from_yaml

config = fetch_config_from_yaml('config.yml')

current_directory = os.path.dirname(os.path.abspath(__file__))
pkl = f"trained_models/{config['model']['name']}_{config['model']['version']}.pkl"
model_path = os.path.join(current_directory, pkl)
model = load(model_path)

def predict(texts):
    predictions = model.predict(texts)
    return [pred for pred in predictions]

if __name__ == "__main__":
    sample_texts = ["I love this!", "I hate this...", "I live in London."]
    preds = predict(sample_texts)
    print(preds)