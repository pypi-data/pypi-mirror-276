import typing as t
import numpy as np

from emotion_model import __version__ as _version
from emotion_model.config.core import config
from emotion_model.processing.data_manager import load_pipeline, solo_image_generator

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_emotion_pipe = load_pipeline(file_name=pipeline_file_name)

def make_prediction(
    image_path: str
) -> dict:
    """Make a prediction using a saved model pipeline."""

    # Загрузка и предобработка изображения
    image = solo_image_generator(image_path)
    image = image.reshape(*config.nn_config.image_reshape_params)

    # Предсказание с использованием модели
    preds = _emotion_pipe.predict(image)
    probs = _emotion_pipe.predict_proba(image)

    emotion_dict = {
        '0': 'surprise',
        '1': 'neutral',
        '2': 'sad',
        '3': 'happy',
        '4': 'anger'
    }

    # Формирование словаря с результатами
    results: t.Dict[str, t.Any] = {
        "preds_ind": int(preds[0]),
        "preds_name": str(emotion_dict[f'{preds[0]}']),
        "probs": [float(np.max(prob)) for prob in probs],
        "version": _version,
        "errors": None
    }

    return results

# print(make_prediction('C:\\Users\\anton\\Desktop\\Documents\\emotion-clf-package\\emotion_model\\dataset\\neutral\\ffhq_18.png'))