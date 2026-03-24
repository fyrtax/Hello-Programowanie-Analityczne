import argparse
import os as os

from ultralytics import YOLO


def download_yolo_network(model_name: str, directory: str) -> YOLO:
    """
    Downloads the specified YOLO network model.

    Args:
        model_name (str): The name of the YOLO model to download. Use names like: 'yolo8n', 'yolo11s', 'yolo11m', 'yolo11m-seg', ...
        directory (str): The directory where the model should be saved.

    Returns:
        An instance of the YOLO class with the specified model loaded.
    """
    yolo_model = YOLO(os.path.join(directory, model_name))
    return yolo_model


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YOLO network model")
    parser.add_argument("-y", "--yolo", type=str, required=True, help="Name of yolo network to download")
    parser.add_argument("-d", "--directory", type=str, required=True, help="Path to directory to save the model")
    args = parser.parse_args()
    model = download_yolo_network(args.yolo, args.directory)
