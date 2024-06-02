# Experimentation Example

## Workflow

1. Import required data via versioned repository.
`dvc import https://git.inf.h-brs.de/mi-project/demo-pipeline/data-annotation-example data/field_A/2023/ -o data/field_A/2023`
2. Other added data should be manually versioned using `dvc add datapath`
3. Reproduce current model training and evaluation using `dvc repro`.
4. Alter `dvc.yaml` for new data input paths, or `params.yaml` for different training configuration.

## Tools

### DVC

Data Versioning and Reproducible pipelines.

### MLFlow

Experiment tracking and model registry.

### Pre Commit Hooks

Clear formated and linted code.

## Insights

- VirtualEnv
Always install virtualenv with `python -m venv`.
Else weird behavior can happen. e.g. `virtualenv venv`

- MLFLow pyfunc
Loaded model expects input in numpy format, instead of torch tensors.

- DVC and MLFlow integration
MLflow generates random run_ids, which need to be tracked if reproducible pipelines should be set up with dvc.
Direct integration was not possible, therefore a workaround with a temporary file had to be implemented.

The output of the training stage is currently not tracked.
