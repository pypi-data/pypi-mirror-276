import json
import os
import shutil
import random
import argparse
import yaml


def split_data(target_files, split_ratio):

    # Random shuffle
    random.shuffle(target_files)

    split_index = int(len(target_files) * split_ratio)
    return target_files[:split_index], target_files[split_index:]


def copy_files(targets, dataset_type, input_path, output_path):
    """Copies the target files and images to the output directory.
    The target files have to contain the path to the image file.

    Args:
        targets (_type_): _description_
        dataset_type (_type_): _description_
    """
    for target in targets:
        with open(os.path.join(input_path, "targets", target), "r") as f:
            target_data = json.load(f)
            image_path = target_data["imagePath"]

        target_dir = os.path.join(output_path, dataset_type, "targets")
        image_dir = os.path.join(output_path, dataset_type, "images")

        os.makedirs(target_dir, exist_ok=True)
        os.makedirs(image_dir, exist_ok=True)

        shutil.copy(
            os.path.join(input_path, "targets", target),
            os.path.join(target_dir, target),
        )
        shutil.copy(
            os.path.join(input_path, image_path),
            os.path.join(image_dir, os.path.basename(image_path)),
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, default=None)
    parser.add_argument("--output_path", type=str, default=None)
    args = parser.parse_args()

    params = yaml.safe_load(open("params.yaml"))["prepare"]

    random.seed(params.get("seed"))

    target_files = os.listdir(os.path.join(args.input_path, "targets"))

    train_targets, test_targets = split_data(target_files, params.get("train_split"))

    # Copy train and test data into separate directories
    copy_files(train_targets, "train", args.input_path, args.output_path)
    copy_files(test_targets, "test", args.input_path, args.output_path)
