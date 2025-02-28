from pathlib import Path
import shutil

import pytest

from digipathos_downloader.download import (create_basic_folder_structure,
                                            create_dir, 
                                            download_zip, 
                                            download_zips, 
                                            fetch_zips_table, 
                                            get_dataset,
                                            remove_tmp_dir,
                                            unpack_zip,
                                            unpack_zips,
                                            validate_downloads)


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
    """assert it is possible to download a sample  

    Args:
        short_zips_table (list): mock fetch_zips return.
    """
    # create tmp folder
    tests_folder = Path(__name__).absolute().parent / 'test'
    tmp_folder = tests_folder / 'tmp'    
    tmp_folder.mkdir()
    
    # gets the metadata from one sample
    sample = short_zips_table[0]

    # download that sample
    ok_url = download_zip(sample["bsLink"], 
                         sample["name"],
                         str(tmp_folder))

    # get path for the downloaded sample
    downloaded_file = list(tmp_folder.iterdir())[0]
    
    # assert the sample exists
    assert str(downloaded_file) == str(tmp_folder / sample["name"])
    
    # assert if download is ok, function returns none
    assert ok_url == None
    
    # remove generated elements by test 
    downloaded_file.unlink()
    tmp_folder.rmdir()

def test_download_zip_return(short_zips_table):
    """assert return is not none when sample download fails.

    Args:
        short_zips_table (list): mock fetch_zips return.
    """
    # gets the metadata from one sample
    sample = short_zips_table[0]

    # broken link
    broken_link = 'https://www.digipathos-rep.cnptia.embrapa.br/jurubeba'

    # download that sample
    not_downloaded = download_zip('jurubeba', 
                                  sample["name"])

    assert not_downloaded == broken_link

def test_download_zips(short_zips_table):
    """assert download_zips can download samples

    Args:
        short_zips_table (list): mock fetch_zips return.
    """
    # create tmp folder
    tests_folder = Path(__name__).absolute().parent / 'test'
    tmp_folder = tests_folder / 'tmp'    
    tmp_folder.mkdir()

    # download samples
    not_downloaded = download_zips(short_zips_table,
                                   str(tmp_folder))
    
    # assert all elements were succesfully downloaded:
    assert not_downloaded == None

    # get downloaded objects
    downloaded_elements = list(tmp_folder.iterdir())

    # generate expected files names
    expected_files = []
    for expected in short_zips_table:
        expected_file = tmp_folder / expected['name']
        expected_files.append(expected_file)

    # assert the samples were succesfully downloaded
    assert set(downloaded_elements) == set(expected_files)

    # remove downloaded samples and folder
    for file in downloaded_elements:
        file.unlink()
    tmp_folder.rmdir()
    
def test_no_zips_downloaded(broken_zips_table):
    # create tmp folder
    tests_folder = Path(__name__).absolute().parent / 'test'
    tmp_folder = tests_folder / 'tmp'    
    tmp_folder.mkdir()

    # download samples
    not_downloaded = download_zips(broken_zips_table,
                                   str(tmp_folder))
    
    # assert no element were downloaded:
    assert len(not_downloaded) == 3    

def test_validate_downloads(short_zips_table):
    """_summary_

    Args:
        short_zips_table (list): mock fetch_zips return.    """
    # create tmp folder
    tests_folder = Path(__name__).absolute().parent / 'test'
    tmp_folder = tests_folder / 'tmp'    
    tmp_folder.mkdir()

    # download samples
    download_zips(short_zips_table,
                  str(tmp_folder))

    # call download validation
    n_zips_in_tmp, zero_size_files = validate_downloads(len(short_zips_table),
                                                        str(tmp_folder),
                                                        False)
    
    assert n_zips_in_tmp == len(short_zips_table)
    assert len(zero_size_files) == 0

    # get downloaded objects
    downloaded_elements = list(tmp_folder.iterdir())

    # remove downloaded samples and folder
    for file in downloaded_elements:
        file.unlink()
    tmp_folder.rmdir()

def test_validate_downloads_null_files(short_zips_table):
    """_summary_

    Args:
        short_zips_table (list): mock fetch_zips return.
    """

    # create tmp folder
    tests_folder = Path(__name__).absolute().parent / 'test'
    tmp_folder = tests_folder / 'tmp'    
    tmp_folder.mkdir()    

    # create fake files
    for file in short_zips_table:
        filepath = tmp_folder / file['name']
        filepath.touch()

    # call download validation
    n_zips_in_tmp, zero_size_files = validate_downloads(len(short_zips_table),
                                                        str(tmp_folder),
                                                        False)
    
    # assert file size is wrong
    assert len(zero_size_files) == 3

    # remove downloaded samples and folder
    for file in tmp_folder.iterdir():
        file.unlink()
    tmp_folder.rmdir()

def test_files_extraction(short_zips_table):
    """validates it is possible to extract a zip

    Args:
        short_zips_table (list): mock fetch_zips return.
    """
    # create tmp folder
    plant_disease_folder = Path(__name__).absolute().parent / 'plant-disease-db'
    plant_disease_folder.mkdir()
    tmp_folder = Path(__name__).absolute().parent / 'tmp'
    tmp_folder.mkdir()

    # gets the metadata from one sample
    sample = short_zips_table[0]

    # download that sample
    ok_url = download_zip(sample["bsLink"], 
                        sample["name"],
                        str(tmp_folder))   
    
    # get downloaded file name
    downloaded_files = list(tmp_folder.iterdir())

    ok_unzip = unpack_zip(str(downloaded_files[0].name),
                          str(plant_disease_folder),
                          str(tmp_folder)) 

    # if unzip is ok, return none
    assert ok_unzip == None

    # assert the folder was successfully created
    extracted_folder = plant_disease_folder / downloaded_files[0].name[:-4]
    assert extracted_folder.exists()

    # assert the files were unzipped 
    extracted_files = list(extracted_folder.iterdir())
    assert len(extracted_files) > 0

    shutil.rmtree(tmp_folder)
    shutil.rmtree(plant_disease_folder)

def test_unpack_fails():
    """assert when unpack fails, the object name is returned
    """

    # create tmp folder
    plant_disease_folder = Path(__name__).absolute().parent / 'plant-disease-db'
    plant_disease_folder.mkdir()
    tmp_folder = Path(__name__).absolute().parent / 'tmp'
    tmp_folder.mkdir()

    # create mock file
    mock_zip = tmp_folder / 'mock.zip'
    mock_zip.touch()

    # tries to unpack an non-existent file
    wrong_file = unpack_zip('wrong_file_path.zip',
                            str(plant_disease_folder),
                            str(tmp_folder))    
    
    # tries unpacking invalid zip
    invalid_zip = unpack_zip('mock.zip',
                             str(plant_disease_folder),
                             str(tmp_folder))

    # validate the messages were returned
    assert type(wrong_file) == str
    assert type(invalid_zip) == str

    shutil.rmtree(plant_disease_folder)
    shutil.rmtree(tmp_folder)

def test_unpack_several_zips(short_zips_table):
    """assert unpacking works for all the zips. 

    Args:
        short_zips_table (list): mock fetch_zips return.
    """

    # create tmp folder
    plant_disease_folder = Path(__name__).absolute().parent / 'plant-disease-db'
    plant_disease_folder.mkdir()
    tmp_folder = Path(__name__).absolute().parent / 'tmp'
    tmp_folder.mkdir()

    # download samples
    not_downloaded = download_zips(short_zips_table,
                                    str(tmp_folder))

    failed_unpack = unpack_zips(str(tmp_folder),
                                str(plant_disease_folder),
                                True)

    # assert all files are successfully unpacked
    assert failed_unpack == None

    # assert all three zips were unpacked
    extracted_folders = list(plant_disease_folder.iterdir())
    assert len(extracted_folders) == 3

    # assert all unpacked folders are non empty
    for folder in extracted_folders:
        extracted = list(folder.iterdir())
        assert len(extracted) > 0

    # clean the mess
    shutil.rmtree(plant_disease_folder)
    shutil.rmtree(tmp_folder)

def test_unzip_samples_fails(mocker):
    """assert failing unzip returns non-empty list.

    Args:
        mocker (_type_): object to mock unpack_zip return
    """

    # create tmp folder
    plant_disease_folder = Path(__name__).absolute().parent / 'test' / 'plant-disease-db'
    plant_disease_folder.mkdir()
    tmp_folder = Path(__name__).absolute().parent / 'test' / 'tmp'
    tmp_folder.mkdir()

    # create fake zips
    fake_1 = tmp_folder / 'a.zip'
    fake_2 = tmp_folder / 'b.zip'
    fake_3 = tmp_folder / 'c.zip'
    fake_1.touch()
    fake_2.touch()
    fake_3.touch()

    # mocks unpack_zip return as a broken unzip
    mocker.patch("digipathos_downloader.download.unpack_zip", return_value='mock.zip')

    # run unpack_zips()
    failed_unpack = unpack_zips(str(tmp_folder),
                                str(plant_disease_folder),
                                True)
    
    # assert unpack_zips return a non-empty list
    assert type(failed_unpack) == list
    assert len(failed_unpack) == 3

    # clean the mess
    shutil.rmtree(plant_disease_folder)
    shutil.rmtree(tmp_folder)    

def test_remove_tmp_dir():
    """assert tmp dir removal.
    """

    # create tmp folder
    tmp_folder = Path(__name__).absolute().parent / 'test' / 'tmp'
    tmp_folder.mkdir() 
    
    # remove dir
    remove_tmp_dir(str(tmp_folder)) 
    
    # assert dir was removed
    assert not tmp_folder.exists() 

def test_get_dataset(mocker,short_zips_table):
    """Assert get_dataset correctly installs the dataset.

    Args:
        mocker (_type_): pytest mocker obj.
        short_zips_table (_type_): fixture mocking fetch_zips_table return.
    """
    # define dataset_dir and tmp_dir
    test_folder = Path(__name__).absolute().parent / 'test' 
    dataset_dir = test_folder / 'dataset_dir'
    tmp_dir = test_folder / 'tmp'

    # mock fetch_zips_table return
    mocker.patch("digipathos_downloader.download.fetch_zips_table", return_value=short_zips_table)
    get_dataset(str(dataset_dir),
                str(tmp_dir),
                "cropped",
                False)
    
    # assert unziped downloads folders are not empty
    downloaded_folders = list(dataset_dir.iterdir())
    for fldr in downloaded_folders:
        list_of_files = list(fldr.iterdir())
        assert len(list_of_files) > 0 
    
    # clean the mess
    shutil.rmtree(str(dataset_dir))
    