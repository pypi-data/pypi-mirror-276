#!/bin/python3
import copy
import json
import logging
import os
import shutil
from typing import Iterable

import numpy as np
import tensorflow
import tensorflow.keras.backend as K


def setup_logger(folder: str = "log") -> None:
    """
    Set up a logger that writes log messages to a file and the console.

    This function creates a logger that writes log messages to a specified
    file and the console. The log messages include a timestamp, the logger's
    name, the severity level of the log message, and the message itself.

    Parameters:
        - folder (str): The directory where the log file will be created. Defaults to "log".

    Returns:
        logging.Logger: Configured logger instance.

    Example:
        .. code-block:: python

            logger = setup_logger()
            logger.info("This is an info message.")
    """
    # Check if logger with the same name already exists
    logger = logging.getLogger(__name__)
    if logger.handlers:
        # Logger already configured, return it
        return logger

    filename = "buas_cv6.log"
    path = os.path.join(folder, filename)
    os.makedirs(folder, exist_ok=True)

    # Create a logger object
    logger = logging.getLogger(__name__)

    # Set the logging level
    logger.setLevel(logging.INFO)

    # Create a handler for writing to a file
    file_handler = logging.FileHandler(path)

    # Create a handler for writing to the console
    console_handler = logging.StreamHandler()

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()


def f1(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
    """
    Calculate the F1 score.

    F1 score is the harmonic mean of precision and recall.
    It's a commonly used metric in binary classification tasks.

    Parameters:
        - y_true (Iterable[float]): True labels.
        - y_pred (Iterable[float]): Predicted labels.

    Returns:
        float: The F1 score.
    """

    def recall_m(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
        y_true = tensorflow.cast(y_true, tensorflow.float32)
        y_pred = tensorflow.cast(y_pred, tensorflow.float32)
        TP = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        Positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = TP / (Positives + K.epsilon())
        return recall

    def precision_m(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
        y_true = tensorflow.cast(y_true, tensorflow.float32)
        y_pred = tensorflow.cast(y_pred, tensorflow.float32)
        TP = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        Pred_Positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = TP / (Pred_Positives + K.epsilon())
        return precision

    try:
        precision, recall = precision_m(y_true, y_pred), recall_m(y_true, y_pred)
    except ValueError:
        logger.error(
            f"An ValueError occurred while calculating precision and recall due to mismatched shapes between {y_true.shape = } and {y_pred.shape =}."
        )

    f1_score = 2 * ((precision * recall) / (precision + recall + K.epsilon()))
    return f1_score


def iou(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
    """
    Calculate the Intersection over Union (IoU) score.

    Intersection over Union (IoU) is a measure used to evaluate the
    overlap between two boundaries. In the context of object detection
    or segmentation, it's used to evaluate the accuracy of predicted
    bounding boxes or segmentations against the ground truth.

    Parameters:
        - y_true (Iterable[float]): True labels.
        - y_pred (Iterable[float]): Predicted labels.

    Returns:
        float: The IoU score.
    """

    def f(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
        y_true = tensorflow.cast(y_true, tensorflow.float32)
        y_pred = tensorflow.cast(y_pred, tensorflow.float32)
        intersection = K.sum(K.abs(y_true * y_pred), axis=[1, 2, 3])
        total = K.sum(K.square(y_true), [1, 2, 3]) + K.sum(K.square(y_pred), [1, 2, 3])
        union = total - intersection
        return (intersection + K.epsilon()) / (union + K.epsilon())

    try:
        iou_ = K.mean(f(y_true, y_pred), axis=-1)
        logger.debug(f"iou return value - {iou_}")
    except ValueError:
        logger.error(
            f"An ValueError occurred while calculating iou due to mismatched shapes between {y_true.shape = } and {y_pred.shape =}."
        )
    return iou_


def clear_destination_folder(image_patch_path: str) -> None:
    """
    Clears the destination folder where the image patch is located. If the folder exists,
    it is removed along with its contents. A new empty folder is then created in the same location.

    Parameters:
        - image_patch_path (str): The file path to the image patch. The folder containing this file will be cleared.

    Returns:
        None
    """
    folder_path = os.path.dirname(image_patch_path)
    if os.path.exists(folder_path):
        logger.info("Clearing destination folder")
        shutil.rmtree(folder_path)
        logger.debug(f"clear_destination_folder - Removing folder: {folder_path}")
    # Create the folder if it doesn't exist
    os.makedirs(folder_path)
    # print(f'Creating folder: {folder_path}')


def mean_confidence_score(predicted_probs: np.ndarray, threshold: float = 0.5) -> float:
    """
    Calculates the mean confidence score of the predicted probabilities that exceed a given threshold.

    Parameters:
        - predicted_probs (Union[np.ndarray, Any]): A numpy array or similar structure containing the predicted probabilities.
        - threshold (float, optional): The threshold above which the predicted probabilities are considered. Default is 0.5.

    Returns:
        - np.ndarray: The mean confidence score of the pixels above the threshold.
    """
    root_pixels = predicted_probs[predicted_probs > threshold]
    return float(np.mean(root_pixels)) if root_pixels.size > 0 else float(0)


def create_config_json(params) -> None:
    logger.info(f"main - writing parameters to model_cofig.json - {params}")

    path_config_json = r"./models/model_config.json"
    model_name = params["model_name"]
    # Create a copy of params and exclude the last item
    params_copy = copy.deepcopy(params)
    params_copy.pop("model_name")

    # Load existing parameters from JSON file if it exists
    try:
        with open(path_config_json, "r", encoding="utf-8") as json_load:
            config_dict = json.load(json_load)

        # Append params to the dictionary in the config file
        if model_name in config_dict:
            logger.error(f"main - Model with name: {model_name} already exists.")
        else:
            config_dict[model_name] = [params_copy]

        with open(path_config_json, "w", encoding="utf-8") as json_dump:
            json.dump(config_dict, json_dump)

    except FileNotFoundError:
        # Create a new dictionary with model_name as key and params as the value
        config_dict = {model_name: [params_copy]}

        with open(path_config_json, "w", encoding="utf-8") as json_file:
            json.dump(config_dict, json_file)
