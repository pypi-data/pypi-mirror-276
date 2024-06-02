import torch
import torch.nn as nn
import torch.optim as optim
from torchinfo import summary
import numpy as np
import argparse
import yaml
import torch
from torch.utils.data import Dataset
from PIL import Image
import json
import os
from torch.utils.data import DataLoader
from torchvision import transforms
import mlflow


class TreeStumpDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.targets = os.listdir(os.path.join(data_dir, "targets"))

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, idx):
        with open(os.path.join(self.data_dir, "targets", self.targets[idx]), "r") as f:
            target_data = json.load(f)
            image_path = target_data["imagePath"]

        image = Image.open(
            os.path.join(self.data_dir, "images", os.path.basename(image_path))
        )
        target = target_data["shapes"][0]["bbox"]

        if self.transform:
            image, target = self.transform(image, target)

        return image, target


def transform(image, bbox):
    # Convert image to tensor and normalize to [0, 1]
    transform_image = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )
    image = transform_image(image)

    # Convert bounding box to tensor and normalize to [0, 1]
    bbox = torch.tensor(bbox) / torch.tensor(
        [image.shape[2], image.shape[1], image.shape[2], image.shape[1]]
    )

    return image, bbox


def reverse_transform(transformed_image, transformed_bbox):
    # Reverse the bounding box normalization
    bbox = transformed_bbox * torch.tensor(
        [
            transformed_image.shape[2],
            transformed_image.shape[1],
            transformed_image.shape[2],
            transformed_image.shape[1],
        ]
    )

    # Reverse the image normalization
    reverse_transform_image = transforms.Compose(
        [transforms.Normalize((-0.5, -0.5, -0.5), (2, 2, 2)), transforms.ToPILImage()]
    )
    image = reverse_transform_image(transformed_image)

    return image, bbox


def get_dataset_loader(data_dir, transform=None, batch_size=10):
    return DataLoader(
        TreeStumpDataset(data_dir, transform=transform),
        batch_size=batch_size,
        shuffle=False,
    )


def get_model():
    # Define the model architecture
    class BoundingBoxModel(nn.Module):
        def __init__(self):
            super(BoundingBoxModel, self).__init__()
            self.conv1 = nn.Conv2d(
                3, 16, 3
            )  # 2D Convolutional layer with 3 input channels and 16 output channels with a kernel size of 3
            self.conv2 = nn.Conv2d(16, 32, 3)
            self.fc1 = nn.Linear(32 * 48 * 48, 256)  # Adjusted for 200x200 input image
            self.fc2 = nn.Linear(256, 4)  # 4 output for bounding box coordinates

        def forward(self, x):
            x = nn.functional.relu(self.conv1(x))
            x = nn.functional.max_pool2d(x, 2)
            x = nn.functional.relu(self.conv2(x))
            x = nn.functional.max_pool2d(x, 2)
            x = x.view(-1, 32 * 48 * 48)  # Adjusted for 200x200 input image
            x = nn.functional.relu(self.fc1(x))
            x = self.fc2(x)
            return x

    return BoundingBoxModel()


def calculate_iou(boxA, boxB):
    # Determine the (x, y)-coordinates of the intersection rectangle

    # Set torch or numpy based on input type
    if isinstance(boxA, torch.Tensor):
        torch_type = True
    else:
        torch_type = False

    if torch_type:
        boxA = boxA.squeeze()
        boxB = boxB.squeeze()
        xA = torch.max(boxA[0], boxB[0])
        yA = torch.max(boxA[1], boxB[1])
        xB = torch.min(boxA[2], boxB[2])
        yB = torch.min(boxA[3], boxB[3])

        # Compute the area of intersection rectangle
        interArea = torch.max(torch.tensor(0), xB - xA) * torch.max(
            torch.tensor(0), yB - yA
        )
    else:
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        # Compute the area of intersection rectangle
        interArea = max(0, xB - xA) * max(0, yB - yA)

    # Compute the area of both the prediction and ground-truth rectangles
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    # Compute the intersection over union by taking the intersection area and dividing it by the sum of prediction + ground-truth areas - the intersection area
    iou = interArea / (boxAArea + boxBArea - interArea)

    return iou


def calculate_iou_batch(boxesA, boxesB):

    ious = []
    for boxA, boxB in zip(boxesA, boxesB):
        iou = calculate_iou(boxA, boxB)
        ious.append(iou)

    # Calc mean iou
    if isinstance(boxesA, torch.Tensor):
        return torch.mean(torch.stack(ious)).item()
    else:
        return np.mean(ious)


def train(model, train_loader, criterion, optimizer, metric_fn, params):

    for epoch in range(params.get("epochs")):
        for batch_idx, (input_data, target) in enumerate(train_loader):
            optimizer.zero_grad()
            output = model(input_data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            metric = metric_fn(output, target)

            # Log metrics
            if epoch % 10 == 0:
                mlflow.log_metric("loss", f"{loss:3f}", step=epoch)
                mlflow.log_metric("log_loss", f"{torch.log10(loss):3f}", step=epoch)
                mlflow.log_metric("IoU", f"{metric:3f}", step=epoch)

            print(
                f"Epoch [{epoch+1}/{params.get('epochs')}], Step [{batch_idx+1}/{len(train_loader)}], Running-Loss: {loss.item()}, Metric: {metric}"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str)
    args = parser.parse_args()

    params = yaml.safe_load(open("params.yaml"))["train"]

    # Set seeds
    np.random.seed(params.get("seed"))
    torch.manual_seed(params.get("seed"))

    # Setup model training
    train_loader = get_dataset_loader(
        args.data_dir, transform=transform, batch_size=params.get("batch_size")
    )

    model = get_model()
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=params.get("learning_rate"))
    metric_fn = calculate_iou_batch

    os.makedirs("tmp", exist_ok=True)
    # Execute model training
    with mlflow.start_run():
        logged_params = {
            "EPOCHS": params.get("epochs"),
            "learning_rate": params.get("learning_rate"),
            "batch_size": params.get("batch_size"),
            "loss_function": criterion.__class__.__name__,
            "metric_function": metric_fn.__name__,
            "optimizer": "SGD",
            "seed": params.get("seed"),
        }

        mlflow.log_params(logged_params)
        with open("tmp/summary.txt", "w") as f:
            f.write(str(summary(model)))
        mlflow.log_artifact("tmp/summary.txt")

        train(model, train_loader, criterion, optimizer, metric_fn, params)

        mlflow.pytorch.log_model(model, "model")

        # Print mlflow run id
        run_id = mlflow.active_run().info.run_id
        print(f"MLflow run_id: {run_id}")
        # Write the run ID to a file
        with open("tmp/mlflow_run_id.txt", "w") as file:
            file.write(run_id)
