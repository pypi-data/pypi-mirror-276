"""Functional interface for datasets.

This module provides a functional interface to interact with datasets.

"""

from .dataset import Dataset
from .dataset_description import DatasetDescription
import logging
from typing import Any
logger = logging.getLogger(__name__)


def open_dataset(name: str, download: bool = True) -> Dataset:
    """Opens and decodes a dataset given its name.

    Notes:
    This function opens the dataset and returns a Dataset object. The dataset
    is not loaded into memory, and its contents are lazy-loaded. Use
    [](`~behaverse.data.load_dataset`) to load the dataset into memory.

    Args:
        name: Name of the dataset to open.
        download: Whether to download the dataset if it is not available locally.

    Returns:
        Dataset: Opened dataset.

    """
    return Dataset.open(name, download)


def load_dataset(name: str, **conditions: Any) -> Dataset:
    """Open the dataset, load content into memory, and close its file handles.

    Notes:
    This is a wrapper around [](`~behaverse.data.open_dataset`). The difference is
    that it loads the Dataset into memory, closes the file, and returns the Dataset.
    In contrast, [](`~behaverse.data.open_dataset`) keeps the file handle open and lazy loads its contents.

    Args:
        name: Name of the dataset to load.
        conditions (dict): Additional conditions passed to `where()`, e.g., `subject_id=['001', '002']`.

    Returns:
        Dataset: The newly loaded dataset.

    Examples:
        To fully load the dataset with the name `P500_9subjects/L1m`:
        ```python
        dataset = load_dataset('P500_9subjects/L1m')
        ```

        To load a dataset with the name `P500_9subjects/L1m` and select
        a subset of subjects by their IDs:
        ```python
        dataset = load_dataset('P500_9subjects/L1m', subject_id=['001', '002'])
        ```

    """
    return Dataset.open(name).where(**conditions).load()


def describe_dataset(dataset: Dataset) -> DatasetDescription:
    """Describe the dataset with the given name.

    Args:
        dataset: Dataset to describe.

    Returns:
        DatasetDescription: Metadata and description of the dataset.

    """
    return dataset.describe()


def validate_dataset(name: str) -> bool:
    """Validate the dataset with the given name.

    Args:
        name: Name of the dataset to validate.

    Returns:
        bool: True if the dataset is valid, False otherwise.

    """
    raise NotImplementedError('Not implemented yet.')
