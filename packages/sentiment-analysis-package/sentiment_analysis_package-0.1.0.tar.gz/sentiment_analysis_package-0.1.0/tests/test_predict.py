from sentiment_model.predict import predict


def test_predict():
   text = ["I love this!", "I hate this...", "I live in London"]
   preds = predict(text)
   assert preds[0] == "Positive"
   assert preds[1] == "Negative"
   assert preds[2] == "Neutral"
