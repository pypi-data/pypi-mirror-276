from sentiment_analysis_model.predict import predict


def test_predict():
   text = ["I love this!", "I hate this..."]
   preds = predict(text)
   assert preds[0] == "positive"
   assert preds[1] == "negative"
