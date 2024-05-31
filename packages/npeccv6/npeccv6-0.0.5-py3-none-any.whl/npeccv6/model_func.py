#!/bin/python3
import argparse
import copy
import csv
import datetime
import json
import os
from typing import Tuple

import cv2
import keras
import numpy as np
import wandb
from tensorflow.keras.callbacks import (EarlyStopping, ModelCheckpoint,
                                        TensorBoard)
from tensorflow.keras.layers import (Conv2D, Conv2DTranspose, Dropout, Input,
                                     MaxPooling2D, concatenate)
from tensorflow.keras.models import Model, load_model
from wandb.integration.keras import WandbMetricsLogger, WandbModelCheckpoint

try:
    # Attempt relative imports (if run as a package module)
    from .data import crop_to_petri, padder
    from .predict import predict
    from .utils import create_config_json, f1, iou, setup_logger

except ImportError:
    # Fallback to absolute imports (if run as a standalone script)
    from predict import predict
    from utils import create_config_json, f1, iou, setup_logger

    from data import crop_to_petri, padder

logger = setup_logger()


def create_model(
    input_shape: Tuple[int] = (256, 256, 1),
    output_classes: int = 1,
    optimizer: str = "adam",
    loss: str = "binary_crossentropy",
    output_activation: str = "sigmoid",
    dropout_1: int = 0.1,
    dropout_2: int = 0.2,
    dropout_3: int = 0.3,
    summary: bool = False,
) -> keras.models.Model:
    """
    Create a U-Net model for semantic segmentation.

    Parameters:
        - input_shape (Tuple[int]): Input shape for the model. Default is (256, 256, 1)
        - output_classes (int): Number of output classes. Default is 1.
        - optimizer (str/optimizer): Name of the optimizer to use or a custom optimizer. Default is 'adam'.
        - loss (str/loss function): Loss function to use during training. Default is 'binary_crossentropy'.
        - output_activation (str): Activation function for the output layer. Default is 'sigmoid'.
        - dropout_1 (float): Dropout rate for the first set of layers. Default is 0.1.
        - dropout_2 (float): Dropout rate for the second set of layers. Default is 0.2.
        - dropout_3 (float): Dropout rate for the third set of layers. Default is 0.3.
        - summary (bool): Whether to print the model summary. Default is False.

    Returns:
        - tensorflow.keras.models.Model: U-Net model for semantic segmentation.
    """
    # Define the logger

    # Build the model
    inputs = Input(input_shape)
    s = inputs

    # Log input shape
    logger.debug(f"Input shape: {input_shape}")

    # Contraction path
    c1 = Conv2D(
        16, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(s)
    c1 = Dropout(dropout_1)(c1)
    c1 = Conv2D(
        16, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c1)
    p1 = MaxPooling2D((2, 2))(c1)

    c2 = Conv2D(
        32, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(p1)
    c2 = Dropout(dropout_1)(c2)
    c2 = Conv2D(
        32, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c2)
    p2 = MaxPooling2D((2, 2))(c2)

    c3 = Conv2D(
        64, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(p2)
    c3 = Dropout(dropout_2)(c3)
    c3 = Conv2D(
        64, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c3)
    p3 = MaxPooling2D((2, 2))(c3)

    c4 = Conv2D(
        128, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(p3)
    c4 = Dropout(dropout_2)(c4)
    c4 = Conv2D(
        128, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c4)
    p4 = MaxPooling2D(pool_size=(2, 2))(c4)

    c5 = Conv2D(
        256, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(p4)
    c5 = Dropout(dropout_3)(c5)
    c5 = Conv2D(
        256, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c5)

    # Expansive path
    u6 = Conv2DTranspose(128, (2, 2), strides=(2, 2), padding="same")(c5)
    u6 = concatenate([u6, c4])
    c6 = Conv2D(
        128, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(u6)
    c6 = Dropout(dropout_2)(c6)
    c6 = Conv2D(
        128, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c6)

    u7 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding="same")(c6)
    u7 = concatenate([u7, c3])
    c7 = Conv2D(
        64, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(u7)
    c7 = Dropout(dropout_2)(c7)
    c7 = Conv2D(
        64, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c7)

    u8 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding="same")(c7)
    u8 = concatenate([u8, c2])
    c8 = Conv2D(
        32, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(u8)
    c8 = Dropout(dropout_1)(c8)
    c8 = Conv2D(
        32, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c8)

    u9 = Conv2DTranspose(16, (2, 2), strides=(2, 2), padding="same")(c8)
    u9 = concatenate([u9, c1], axis=3)
    c9 = Conv2D(
        16, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(u9)
    c9 = Dropout(dropout_1)(c9)
    c9 = Conv2D(
        16, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c9)

    outputs = Conv2D(output_classes, (1, 1), activation=output_activation)(c9)

    model = Model(inputs=[inputs], outputs=[outputs])

    # Compile the model
    model.compile(optimizer=optimizer, loss=loss, metrics=["accuracy", f1, iou])

    # Show model summary
    if summary:
        logger.info(model.summary())

    return model


def load_pretrained_model(model_name: str) -> keras.models.Model:
    """
    Load a saved and pre-trained U-Net model from the specified directory.

    Parameters:
        - model_name (str): The name of the model file to load.

    Returns:
        - tensorflow.keras.models.Model: The loaded U-Net model.

    Raises:
        - FileNotFoundError: If the model file does not exist at the specified path.

    Notes:
        - The model file needs to be in the './models' directory.
    """

    # Construct the model path
    model_path = os.path.join("models/", model_name + ".keras")

    # Check if the model file exists
    if not os.path.exists(model_path):
        logger.error(f"No model found at {model_path} with the name: {model_name}")
        raise FileNotFoundError(
            f"No model found at {model_path} with the name: {model_name}"
        )

    # Load the model
    model = load_model(model_path, custom_objects={"f1": f1, "iou": iou})

    # Log the model being loaded succesfully
    logger.info(f"Model loaded successfully from {model_path}")

    return model


def train_model(
    model_name: str,
    train_generator,
    test_generator,
    steps_per_epoch: int,
    validation_steps: int,
    input_shape: Tuple[int] = (256, 256, 1),
    epochs: int = 20,
    model_suffix: str = "",
    summary: bool = False,
) -> None:
    """
    Trains and saves a convolutional neural network model using the specified architecture.

    Parameters:
        - model_name (str): Name of model selected by user.
        - train_generator: Training data generator.
        - test_generator: Testing data generator.
        - input_shape (int): Input shape used for the model.
        - steps_per_epoch (int): Number of steps to be taken per epoch.
        - validation_steps (int): Number of steps to be taken for validation.
        - epochs (int, optional): Number of training epochs (default is 20).
        - model_suffix (str, optional): Suffix to append to the model filename (default is '').
        - summary (bool, optional): Flag indicating whether to print the model summary (default is False).

    Returns:
        None

    Notes:
        - The function initializes a neural network model based on the specified architecture.
        - Training is performed using the provided data generators and hyperparameters.
        - Early stopping and model checkpoint callbacks are applied during training.
        - The best model is saved to a file with the specified suffix.
    """
    # Check model availability, if not, create new one
    try:
        model = load_pretrained_model(model_name)
        logger.info(f"{model_name} loaded")
    except:
        model = create_model(input_shape)
        logger.info(f"{model_name} created")

    Now = datetime.datetime.now()
    time = Now.strftime("%Y%m%d-%H%M")

    # Start a run, tracking hyperparameters
    wandb.init(
        # Set the wandb project where this run will be logged
        project=model_name,
        # entity="220817",  # Maybe change
        # Track hyperparameters and run metadata with wandb.config
        sync_tensorboard=True,
        config={
            "metric": ["accuracy", f1, iou],
            "epoch": epochs,
            "steps_per_epoch": steps_per_epoch,
        },
    )

    tb = TensorBoard(log_dir="./logs/tensorboard/" + time, histogram_freq=1)
    logger.info(
        f'Tensorboard of {model_name} at location {"./logs/tensorboard/" + time}'
    )
    cb = EarlyStopping(
        monitor="val_loss", patience=5, restore_best_weights="True", mode="min"
    )

    save_model = ModelCheckpoint(
        # f"models/{model_name}{model_suffix}{epochs:02d}.h5",
        f"models/{model_name}.keras",
        save_best_only=True,
        monitor="val_loss",
        mode="min",
        # summary=summary,
    )
    wbml = (WandbMetricsLogger(log_freq="epoch"),)
    # wbmc = WandbModelCheckpoint(filepath = f"./models/wandb/{model_name}", save_best_only=True),

    history = model.fit(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=epochs,
        validation_data=test_generator,
        validation_steps=validation_steps,
        callbacks=[
            cb,
            tb,
            save_model,
            wbml,
            # wbmc
        ],
    )
    wandb.finish()
    os.makedirs("./models/", exist_ok=True)
    model.save("./models/" + time + ".keras")
    logger.info(f'{model_name} saved at location {"./models/" + time}')
    logger.info(f"train_model - history - {history}")

    # Extracting patch_size and color_channels from input_shape
    patch_size = input_shape[0]
    color_channels = input_shape[2]
    best_val_loss = np.min(history.history["val_loss"])

    os.makedirs(r"./log/", exist_ok=True)
    csv_file = "./log/model_info.csv"

    # Check if the file exists to avoid writing headers multiple times
    file_exists = os.path.isfile(csv_file)
    logger.debug(f"train_model - file_exists - {file_exists}")

    logger.debug(
        f"Writing data: {model_name}, {patch_size}, {color_channels}, {best_val_loss}"
    )

    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        # Write header only if file does not exist
        if not file_exists:
            writer.writerow(["Model_name", "patch_size", "color_channels", "val_loss"])
            logger.debug("Header written to CSV")
        writer.writerow([model_name, patch_size, color_channels, best_val_loss])
        logger.debug("Data row written to CSV")


def model_eval(
    model_name: str,
    test_data_dir: str,
    patch_size: int = 256,
) -> Tuple[float, float]:
    """
    Evaluates a pre-trained model on a test dataset of images and their corresponding masks.

    Parameters:
        - model_name (str): The name or path of the pre-trained model to be loaded.
        - test_data_dir (str): The directory containing the test images and masks.
        - patch_size (int): Size of the patches to use.

    Returns:
        Tuple[float, float]:
            A tuple containing the F1 score and IoU (Intersection over Union) score for the model's predictions on the test dataset.

    Notes:
        The function performs the following steps:
        1. Sets up a logger for debugging and logging purposes.
        2. Initializes empty lists to store predictions (preds) and ground truth masks (y_true).
        3. Loads the specified pre-trained model.
        4. Iterates through each file in the test data directory:
            - Checks if the file is a PNG image.
            - Constructs the file path for the image and its corresponding mask.
            - Reads the mask image using OpenCV.
            - Uses the model to predict the mask for the image.
            - Appends the predicted mask and the ground truth mask to their respective lists.
        5. Calculates the F1 score and IoU score using the ground truth masks and the model's predictions.
        6. Logs and returns the F1 score and IoU score as a tuple.
    """
    # Set up logger
    logger = setup_logger()

    # Create path to masks and images
    test_data_folder_list = os.listdir(test_data_dir)
    test_data_image_path = os.path.join(test_data_dir, test_data_folder_list[0])
    test_data_mask_path = os.path.join(test_data_dir, test_data_folder_list[1])
    logger.debug(f"model_eval - test_data_image_path - {test_data_image_path}")
    logger.debug(f"model_eval - test_data_mask_path - {test_data_mask_path}")

    # Define empty list for preds
    preds = []

    # Define empty list for y true
    y_true = []

    # Define empty list for confidence score
    conf_scores = []

    # Load model
    model = load_pretrained_model(model_name)

    # Enumerate through test data directory
    for idx, file in enumerate(os.listdir(test_data_image_path)):
        # Check if file is png
        if file.endswith(".png"):
            # Create filepath to image
            file_path_image = os.path.join(test_data_dir, "images", file)
            logger.debug(f"model_eval - file_path_image - {file_path_image}")

            # Split file on . taking the first item
            file_name = file.split(".")[0]
            logger.debug(f"model_eval - file_name - {file_name}")

            # Create filepath to mask
            file_path_mask = os.path.join(
                test_data_dir, "masks", file_name + "_root_mask.tif"
            )
            logger.debug(f"model_eval - file_path_mask - {file_path_mask}")

            # Read mask as image
            mask_im = cv2.imread(file_path_mask, 0)
            logger.debug(f"model_eval - mask_im - {mask_im.shape}")

            # Read image as grayscale
            im = cv2.imread(file_path_image, 0)

            # Predict using model on a single image
            pred, conf = predict(
                model,
                file_path_image,
                r"../predictions/test_image_{}.png".format(idx),
            )

            logger.debug(f"model_eval - pred - {pred.shape}")

            # Extract petri region of interest and apply it to the mask_im
            _, roiX, roiY, roiW, roiH = crop_to_petri(im)
            cropped_mask = mask_im[roiY : roiY + roiH, roiX : roiX + roiW]
            logger.debug(f"model_eval - cropped_mask.shape - {cropped_mask.shape}")

            # Adding padding to the mask
            padded_cropped_mask = padder(cropped_mask, patch_size)

            # Append items to lists
            preds.append(pred)
            y_true.append(padded_cropped_mask)
            conf_scores.append(conf)

    # Convert lists to numpy arrays
    preds = np.array(preds)
    y_true = np.array(y_true)
    conf_scores = np.array(conf_scores)
    logger.debug(f"model_eval - preds.shape - {preds.shape}")
    logger.debug(f"model_eval - y_true.shape - {y_true.shape}")
    logger.debug(f"model_eval - conf_scores.shape - {conf_scores.shape}")

    # Calculate f1
    f1_ = f1(y_true, preds)
    logger.info(f"model_eval - f1 - {f1_}")

    # Calculate iou
    iou_ = iou(y_true, preds)
    logger.info(f"model_eval - iou - {iou_}")

    avg_conf_over_all_preds = np.mean(conf_scores)

    return f1_, iou_, avg_conf_over_all_preds


def main() -> None:
    parser = argparse.ArgumentParser(description="Create model_config.json.")

    parser.add_argument("--input_shape", nargs="+", type=int, default=[256, 256, 1])
    parser.add_argument("--output_classes", type=int, default=1)
    parser.add_argument("--optimizer", type=str, default="adam")
    parser.add_argument("--loss", type=str, default="binary_crossentropy")
    parser.add_argument("--output_activation", type=str, default="sigmoid")
    parser.add_argument("--dropout_1", type=float, default=0.1)
    parser.add_argument("--dropout_2", type=float, default=0.2)
    parser.add_argument("--dropout_3", type=float, default=0.3)
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--model_name", type=str)

    args = parser.parse_args()

    # Store parameters in JSON file
    params = vars(args)

    create_config_json(params=params)


if __name__ == "__main__":
    main()
