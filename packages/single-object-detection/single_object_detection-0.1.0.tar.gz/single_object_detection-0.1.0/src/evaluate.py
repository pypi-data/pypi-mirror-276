import os
import argparse
import mlflow.pytorch
from train import get_dataset_loader, transform, calculate_iou_batch


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_uri", type=str)
    parser.add_argument("--model_uri_file", type=str)
    parser.add_argument("--data_dir", type=str)
    parser.add_argument("--result_dir", type=str)
    args = parser.parse_args()

    # Read run_id from file
    with open(args.model_uri_file, "r") as file:
        run_id = file.read()

    # Insert run_id into model_uri
    model_uri = args.model_uri
    model_uri = model_uri.replace("{mlflow_run_id}", f"{run_id}")

    print(f"Loading model from: {model_uri}")

    model = mlflow.pytorch.load_model(model_uri)
    test_dataset = get_dataset_loader(args.data_dir, transform=transform, batch_size=10)

    # Evaluate the model
    iou_scores = []
    for batch in test_dataset:
        images, targets = batch
        predictions = model(images)

        ious = calculate_iou_batch(predictions, targets)

        iou_scores.append(ious)

    average_iou = sum(iou_scores) / len(iou_scores)
    print(f"Mean IOU: {average_iou}")

    os.makedirs(args.result_dir, exist_ok=True)
    # Write the IOU score to a file
    with open(os.path.join(args.result_dir, "iou_score.txt"), "w") as file:
        file.write(str(average_iou))
