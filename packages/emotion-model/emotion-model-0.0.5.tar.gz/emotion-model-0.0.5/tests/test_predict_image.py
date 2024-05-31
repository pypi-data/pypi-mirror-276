from emotion_model.predict import make_prediction


def test_make_prediction(path):
    expected_len = 5

    res = make_prediction(path)
    preds_ind = res['preds_ind']
    preds_name = res['preds_name']
    probs = res['probs']

    assert isinstance(preds_ind, int)
    assert isinstance(preds_name, str)
    assert isinstance(probs, list)
    assert res['errors'] is None
    assert len(probs) == expected_len
