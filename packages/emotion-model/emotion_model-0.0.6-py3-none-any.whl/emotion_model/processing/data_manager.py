import typing as t
import numpy as np
import os
import joblib
import cv2
from keras import Sequential

from emotion_model import __version__ as _version
from emotion_model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config


def solo_image_generator(path: str) -> t.Any:
    """Helper function to load an image"""

    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.astype('float32') / 255.0
    img = img.flatten()
    img_arr = []
    img_arr.append(img)
    img_arr = np.array(img_arr)
    return img_arr


def image_generator(emotions: list[str]) -> t.Generator:
    """Image loading and initial preprocessing"""

    for index, emotion in enumerate(emotions):
        for filename in os.listdir(os.path.join(DATASET_DIR, emotion)):
            img = cv2.imread(os.path.join(DATASET_DIR, emotion, filename))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = img.astype('float32') / 255.0
            img = img.flatten()
            yield img, index


def load_dataset(emotions: list[str]) -> t.Any:
    """Load the dataset."""

    X, y = [], []
    for img, label in image_generator(emotions):
        X.append(img)
        y.append(label)
    X = np.array(X)
    y = np.array(y)
    return X, y


def save_model(*, model_to_persist: Sequential) -> None:
    """Persist the model.
    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.
    """

    # Prepare versioned save file name
    save_file_name = f"{config.app_config.clf_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    remove_old_models(files_to_keep=[save_file_name])
    joblib.dump(model_to_persist, save_path)


def load_model(*, file_name: str) -> Sequential:
    """Load a persisted model."""

    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model


def remove_old_models(*, files_to_keep: t.List[str]) -> None:
    """
    Remove old models.
    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()
