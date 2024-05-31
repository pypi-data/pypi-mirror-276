import pandas as pd
from joblib import load
from sentiment_model.config.core import fetch_config_from_yaml

config = fetch_config_from_yaml('config.yml')
model = load(f"{config['data']['saving_path']}{config['model']['name']}_{config['model']['version']}.pkl")

def predict(texts):
    predictions = model.predict(texts)
    return [pred for pred in predictions]

if __name__ == "__main__":
    sample_texts = ["I love this!", "I hate this...", "I live in London."]
    preds = predict(sample_texts)
    print(preds)