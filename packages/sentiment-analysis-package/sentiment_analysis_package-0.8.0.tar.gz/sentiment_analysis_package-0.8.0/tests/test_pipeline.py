from sentiment_model.pipeline import create_pipeline

def test_pipeline_creation():
    pipeline = create_pipeline()
    assert pipeline is not None
