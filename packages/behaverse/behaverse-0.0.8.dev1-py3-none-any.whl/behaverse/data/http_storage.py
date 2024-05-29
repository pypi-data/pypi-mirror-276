"""Access Behaverse datasets via HTTP(S) protocol."""

from pathlib import Path
from tqdm.auto import tqdm
import pandas as pd
import requests
import yaml
import logging
from .utils import extract_dataset
logger = logging.getLogger(__name__)


def list_datasets() -> pd.DataFrame:
    """List available datasets.

    Returns:
        DataFrame: List of available datasets including name, short description, and url.

    Notes:
        The list of datasets is stored in a YAML file hosted on GitHub.
        Default URL: https://raw.githubusercontent.com/behaverse/behaverse/Registry/datasets/datasets.yml

    """
    # default url for the list of datasets
    url = 'https://raw.githubusercontent.com/behaverse/behaverse/Registry/datasets/datasets.yml'
    response = requests.get(url)
    if response.status_code == 200:
        datasets = pd.DataFrame(yaml.safe_load(response.text))
        return datasets
    else:
        logger.error(f'Failed to get the list of datasets from {url}.')
        raise Exception(f'Failed to get the list of datasets from {url}.')


def download_dataset(name: str, **kwargs) -> Path:
    """Download dataset from the given URL.

    Args:
        name: the name of the dataset to download.
        kwargs (dict): additional arguments. For example you can specify the destination
                        path (`dest`) to save the dataset file. Defaults to
                        `~/.behaverse/datasets/{name}/`. Or `chunk_size` to specify the chunk size for downloading.

    Returns:
        Path: Path to the downloaded dataset file.
    """
    assert name is not None, 'Dataset name is required.'

    datasets: pd.DataFrame = list_datasets()
    # query datasets for the url of a row with the given name
    download_url = datasets[datasets['name'] == name]['download_url'].values[0]

    dest = Path(kwargs.get('dest',
                           Path.home() / '.behaverse' / 'datasets' / f'{name}.tar.gz'))
    chunk_size = kwargs.get('chunk_size', 8096)

    if dest.exists():
        return extract_dataset(name)

    dest.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()

        with open(dest, 'wb') as f:
            for chunk in tqdm(r.iter_content(chunk_size=chunk_size),
                              leave=False,
                              unit='B'):
                f.write(chunk)

    logger.info(f'Downloaded dataset to {dest}, now extracting...')

    output_path = extract_dataset(name)
    logger.info(f'Extracted dataset to {output_path}')
    return output_path
