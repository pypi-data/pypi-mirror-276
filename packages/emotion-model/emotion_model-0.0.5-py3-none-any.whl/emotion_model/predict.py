import typing as t
import numpy as np

from emotion_model import __version__ as _version
from emotion_model.config.core import config
from emotion_model.processing.data_manager import solo_image_generator, load_model


model_file_name = f"{config.app_config.clf_save_file}{_version}.pkl"
_emotion_clf = load_model(file_name=model_file_name)


def make_prediction(
    image_path: str
) -> dict:
    """Make a prediction using a saved model."""

    image = solo_image_generator(image_path)
    image = image.reshape(*config.nn_config.image_reshape_params)

    probs = _emotion_clf.predict(image)
    emotion_ind = np.argmax(probs)

    emotion_dict = {
        '0': 'surprise',
        '1': 'neutral',
        '2': 'sad',
        '3': 'happy',
        '4': 'anger'
    }

    results: t.Dict[str, t.Any] = {
        "preds_ind": int(emotion_ind),
        "preds_name": str(emotion_dict[f'{emotion_ind}']),
        "probs": [float(prob) for prob in probs[0]],
        "version": _version,
        "errors": None
    }

    return results
