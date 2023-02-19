from pathlib import Path

import pytest

from digipathos_downloader.download import (create_basic_folder_structure,
                                            create_dir, download_zip, download_zips, 
                                            fetch_zips_table)


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
    expected_tmp_folder = tests_folder / 'tmp'
    create_basic_folder_structure(str(expected_dataset_folder), 
                                  str(expected_tmp_folder))
    assert expected_dataset_folder.exists()
    assert expected_tmp_folder.exists()
    expected_tmp_folder.rmdir()
    expected_dataset_folder.rmdir()

def test_create_basic_folder_structure_error():
    """assert similar folder names raise an error.
    """
    tests_folder = Path(__name__).absolute().parent / 'test'
    expected_dataset_folder = tests_folder / 'folder'
    expected_tmp_folder = tests_folder / 'folder'
    with pytest.raises(ValueError):
        create_basic_folder_structure(str(expected_dataset_folder), 
                                      str(expected_tmp_folder))


def test_fetch_zips_table():
    """assert fetch_zip_table generates a non-empty list.
    """
    zips_table = fetch_zips_table('all')
    assert len(zips_table) != 0
    assert type(zips_table) == list

def test_download_zip(short_zips_table):
    # create tmp folder
    tests_folder = Path(__name__).absolute().parent / 'test'
    expected_tmp_folder = tests_folder / 'tmp'    
    expected_tmp_folder.mkdir()
    
    # gets the metadata from one sample
    sample = short_zips_table[0]

    # download that sample
    ok_url = download_zip(sample["bsLink"], 
                         sample["name"],
                         str(expected_tmp_folder))

    # get path for the downloaded sample
    downloaded_file = list(expected_tmp_folder.iterdir())[0]
    
    # assert the sample exists
    assert str(downloaded_file) == str(expected_tmp_folder / sample["name"])
    
    # assert if download is ok, function returns none
    assert ok_url == None
    
    # remove generated elements by test 
    downloaded_file.unlink()
    expected_tmp_folder.rmdir()

def test_download_zip_return(short_zips_table):
    # gets the metadata from one sample
    sample = short_zips_table[0]

    # broken link
    broken_link = 'https://www.digipathos-rep.cnptia.embrapa.br/jurubeba'

    # download that sample
    not_downloaded = download_zip('jurubeba', 
                                  sample["name"])

    assert not_downloaded == broken_link