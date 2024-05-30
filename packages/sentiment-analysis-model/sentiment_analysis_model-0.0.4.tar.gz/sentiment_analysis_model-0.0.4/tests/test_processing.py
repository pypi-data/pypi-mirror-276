from sentiment_analysis_model.processing.features import preprocess_text

def test_preprocess_text():
    sample_text = "This is an example sentence!"
    processed_text = preprocess_text(sample_text)
    assert processed_text == "example sentence"
