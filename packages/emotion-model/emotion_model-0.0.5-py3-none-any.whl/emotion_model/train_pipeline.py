import logging
from pathlib import Path

from emotion_model.config.core import LOG_DIR, config
from emotion_model.emotion_pipeline import emotion_clf
from emotion_model import __version__ as _version
from emotion_model.processing.data_manager import load_dataset, save_model
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


def run_training() -> None:
    """Train the model."""

    log_path = Path(f"{LOG_DIR}/log_{_version}.log")
    if Path.exists(log_path):
        log_path.unlink()
    logging.basicConfig(filename=log_path, level=logging.DEBUG)

    emotions = config.nn_config.emotions

    X, y = load_dataset(emotions)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config.nn_config.test_size,
                                                        random_state=config.nn_config.random_state)
    X_train = X_train.reshape(*config.nn_config.image_reshape_params)
    X_test = X_test.reshape(*config.nn_config.image_reshape_params)

    emotion_clf.fit(X_train, y_train, epochs=config.nn_config.epochs,
                      batch_size=config.nn_config.batch_size)

    save_model(model_to_persist=emotion_clf)

    class_ = emotion_clf.predict(X_train)

    print(classification_report(y_train, class_, target_names=emotions))
    print()

    logging.info(f"train metrics: {classification_report(y_train, class_, target_names=emotions)}")

    class_ = emotion_clf.predict(X_test)

    print(classification_report(y_test, class_, target_names=emotions))
    print()

    logging.info(f"test metrics: {classification_report(y_test, class_, target_names=emotions)}")


if __name__ == "__main__":
    run_training()
