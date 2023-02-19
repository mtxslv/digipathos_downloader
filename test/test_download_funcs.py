from pathlib import Path

import pytest

from digipathos_downloader.download import (create_basic_folder_structure,
                                            create_dir)


def test_create_dir():
    tests_folder = Path(__name__).absolute().parent / 'test'
    print(tests_folder)
    mock_folder = tests_folder / 'mock_folder'
    create_dir(str(mock_folder))
    assert mock_folder.exists()
    mock_folder.rmdir()

