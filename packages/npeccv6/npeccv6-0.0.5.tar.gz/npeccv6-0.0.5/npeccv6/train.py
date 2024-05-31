#!/bin/python3
import argparse

try:
    # Attempt relative imports (if run as a package module)
    from .data import load_and_preprocess_data
    from .model_func import train_model
    from .utils import setup_logger

except ImportError:
    # Fallback to absolute imports (if run as a standalone script)
    from model_func import train_model
    from utils import setup_logger

    from data import load_and_preprocess_data

logger = setup_logger()


def main():
    parser = argparse.ArgumentParser(
        description="Train a U-net model from images and masks."
    )
    parser.add_argument("model_name", help="name of the model.")
    parser.add_argument(
        "-c",
        "--classes",
        default=["root"],
        help="Classes to use to train the model the model. For single class(recomended): ['class'], for multiclass(not advised):['class1', 'class2']",
    )
    parser.add_argument(
        "-d",
        "--patch_dir",
        default="./data_patched/",
        help="Path to data root directory, should end with '/'. Default: './data_patched/'",
    )

    parser.add_argument(
        "-p",
        "--patch_size",
        default=256,
        help="How big patches to use for the model. Default: 256",
    )

    parser.add_argument(
        "-s", "--seed", default=42, help="Seed for reading data and model training"
    )
    parser.add_argument(
        "-b", "--batch_size", default=16, help="What batch size to use. Default: 16"
    )
    parser.add_argument(
        "-o",
        "--color",
        default="grayscale",
        help="What color mode to use. Default: 'grayscale'",
    )
    parser.add_argument(
        "-e", "--epochs", default=20, help="Number of epochs. Default: 20"
    )
    # Disabled
    parser.add_argument(
        "-r",
        "--roots",
        default=5,
        help="DISABLED!!! Number of expected plants inside petri dish. Default: 5",
    )

    args = parser.parse_args()

    patch_size = args.patch_size

    (
        train_generator,
        test_generator,
        steps_per_epoch,
        validation_steps,
    ) = load_and_preprocess_data(
        args.classes,
        args.model_name,
        patch_size,
        args.patch_dir,
        args.seed,
        args.batch_size,
        args.color,
    )

    logger.info(f"Training model\n{steps_per_epoch = }\n{validation_steps = }")

    if args.color == "grayscale":
        color = 1
    else:
        color = 3

    print(patch_size, patch_size, color)
    train_model(
        model_name=args.model_name,
        train_generator=train_generator,
        test_generator=test_generator,
        steps_per_epoch=steps_per_epoch,
        validation_steps=validation_steps,
        input_shape=(patch_size, patch_size, color),
        epochs=args.epochs,
    )


if __name__ == "__main__":
    main()
