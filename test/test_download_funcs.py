from pathlib import Path

import pytest

from digipathos_downloader.download import (create_basic_folder_structure,
                                            create_dir)


def test_create_dir():
    """assert a dir is created.
    """
    tests_folder = Path(__name__).absolute().parent / 'test'
    mock_folder = tests_folder / 'mock_folder'
    create_dir(str(mock_folder))
    assert mock_folder.exists()
    mock_folder.rmdir()

def test_create_basic_folder_structure():
    """assert the folder structure used during download is created.
    """
    tests_folder = Path(__name__).absolute().parent / 'test'
    expected_dataset_folder = tests_folder / 'plant-disease-db'
    expected_tmp_folder = expected_dataset_folder / 'tmp'
    create_basic_folder_structure(str(tests_folder))
    assert expected_dataset_folder.exists()
    assert expected_tmp_folder.exists()
    expected_tmp_folder.rmdir()
    expected_dataset_folder.rmdir()