import os
import shutil
import sys
import zipfile

import requests

BASE_URL = "https://www.digipathos-rep.cnptia.embrapa.br"
LIST_URL = BASE_URL + "/jspui/zipsincollection/123456789/3"

WORKING_DIR = os.getcwd()
DATA_DIR = WORKING_DIR + "/plant-disease-db"
TMP_DIR = DATA_DIR + "/tmp/"


def create_dir(path) -> None:
    """Create directory in a given path.

    Args:
        path (str): the directory to be created. 

    Raises:
        OSError: raised when the directory cannot be created.
    """
    try:
        os.mkdir(path)
    except OSError as e:
        raise OSError(f"{e}\nFailed to create directory: {path}")


def create_basic_folder_structure(dataset_dir: str = 'plant-disease-db', 
                                  volatile_dir: str = 'tmp',  
                                  verbose: str = False) -> None:
    """Create folder structure for the dataset download process.

    Args:
        dataset_dir (str, optional): the name of the  directory where the images will be downloaded to. Defaults to 'plant-disease-db'.
        volatile_dir (str, optional): the name of the directory where temporary files are kept. Cannot be equal to dataset_dir. Defaults to 'tmp'.
        verbose (str, optional): notify the user about the download progress. Defaults to False.

    Raises:
        OSError: raised when the directories cannot be created.
    """
    if dataset_dir == volatile_dir:
        raise ValueError('Directories cannot be the same.')
    data_dir = dataset_dir
    tmp_dir = volatile_dir

    if verbose:
        print("Setting up basic folder structure...")
    try:
        create_dir(data_dir)
        create_dir(tmp_dir)
    except OSError as e:
        print(f"{e}\nUnable to create basic folder structure. Please make sure the directory exists and is empty.")
        sys.exit(1)


def fetch_zips_table(name_filter: str = "cropped", 
                     verbose: str = False,
                     base_url: str = "https://www.digipathos-rep.cnptia.embrapa.br",
                     list_url: str = "/jspui/zipsincollection/123456789/3"):
    """Fetch Zips table. Executes a get request to the digipathos website requesting the the images metadata. 

    Args:
        name_filter (str): which images to download: cropped only, original only, or all. Defaults to 'cropped'.
        verbose (str, optional): notify about the process. Defaults to False.
        base_url (str, optional): digipathos base url. Defaults to "https://www.digipathos-rep.cnptia.embrapa.br".
        list_url (str, optional): digipathos list url. Defaults to "/jspui/zipsincollection/123456789/3".

    Returns: 
        zips_table: a list containing the images' metadata.

    Raises:
        RequestException: raised when the process is unable to fetch zip table from a given image url.
    """
    url = base_url + list_url
    if verbose:
        print("Downloading table containing remote image DB information...")
    query_params = {"offset": 0, "limit": 100000}
    try:
        response = requests.get(url, query_params).json()
    except requests.exceptions.RequestException as e:
        print(f"{e}\nUnable to fetch ZIP's table from {url}")
        sys.exit(1)
    else:
        zips_table = response["bitstreams"]
        if name_filter.lower() == "cropped":
            if verbose:
                print("Filtering for cropped images...")
            return [entry for entry in zips_table if "cropped" in entry["name"].lower()]
        elif name_filter.lower() == "original":
            if verbose:
                print("Filtering for original images...")
            return [entry for entry in zips_table if "cropped" not in entry["name"].lower()]
        else:
            return zips_table


def download_zip(relative_url: str, 
                 zip_name: str, 
                 tmp_dir: str = '.',                 
                 base_url: str = "https://www.digipathos-rep.cnptia.embrapa.br"):
    """Tries to download a sample (a zip file).

    Args:
        relative_url (str): the sample url to be downloaded.
        zip_name (str): the sample name.
        tmp_dir (str): where the zip file will be downloaded to.  
        base_url (str, optional): digipathos base url. Defaults to "https://www.digipathos-rep.cnptia.embrapa.br".
    
    Returns:
        url_not_downloaded (str): the url of a failed download. If download is successful, returns None.
    """
    
    url_not_downloaded = None
    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        try:
            response = requests.get(base_url + relative_url)
            if not response.ok:
                print(f"Error while downloading {zip_name}.\Retrying...")
                attempts += 1
            else:
                break
        except requests.exceptions.RequestException:
            print(f"Error while downloading {zip_name}.\nRetrying...")
            attempts += 1

    if attempts < max_attempts:
        filename = tmp_dir + '/' + zip_name
        try:
            open(filename, "wb").write(response.content)
        except EnvironmentError as e:
            url_not_downloaded = base_url + '/' + relative_url
            print(f"{e}\nFailed to write {zip_name} to {tmp_dir}\n"
                  f"Please try to download it manually: {url_not_downloaded}")
            return url_not_downloaded
    else:
        url_not_downloaded = base_url + '/' + relative_url
        print(f"\nFailed to download {zip_name}\n"
              f"Please try to download it manually: {url_not_downloaded}")
        return url_not_downloaded

def download_zips(zips_tbl, verbose):
    for index, remote_zip_info in enumerate(zips_tbl):
        if verbose:
            print(f"Downloading ZIP-file {index+1}/{len(zips_tbl)}...")
        download_zip(remote_zip_info["bsLink"], remote_zip_info["name"])


def validate_downloads(n_zips, verbose):
    if verbose:
        print("Validating downloads...")
    n_zips_in_tmp = len([name for name in os.listdir(TMP_DIR)])
    if n_zips_in_tmp != n_zips:
        print(f"WARNING: Number of ZIP-files in {TMP_DIR} is not the same as retrieved from the EMPRABA website.\n"
              f"Expected number of ZIP-files: {n_zips}. ZIP-files found in directory: {n_zips_in_tmp}.")
    for filename in os.listdir(TMP_DIR):
        if os.path.getsize(TMP_DIR + filename) == 0:
            print(f"WARNING: ZIP-file {filename} has a size of 0 bytes.")


def unpack_zip(filename):
    class_dir = DATA_DIR + "/" + filename[:-4]
    try:
        create_dir(class_dir)
        with zipfile.ZipFile(TMP_DIR + filename, mode="r") as zip_contents:
            zip_contents.extractall(class_dir)
    except IOError as e:
        print(f"{e}\nSkipping unpacking of {filename}")


def unpack_zips(verbose):
    if verbose:
        print("Unpacking ZIP-files...")
    for zip_file in os.listdir(TMP_DIR):
        unpack_zip(zip_file)


def remove_tmp_dir():
    shutil.rmtree(TMP_DIR)

def get_dataset(name_filter, verbose):
    """Download function for python code.

    Args:
        name_filter (_type_): _description_
        verbose (_type_): _description_
    """
    create_basic_folder_structure(verbose=verbose)
    zips_table = fetch_zips_table(name_filter=name_filter, verbose=verbose)
    download_zips(zips_table, verbose=verbose)
    validate_downloads(len(zips_table), verbose=verbose)
    unpack_zips(verbose=verbose)
    remove_tmp_dir()    

def main(name_filter, verbose):
    create_basic_folder_structure(verbose=verbose)
    zips_table = fetch_zips_table(name_filter=name_filter, verbose=verbose)
    download_zips(zips_table, verbose=verbose)
    validate_downloads(len(zips_table), verbose=verbose)
    unpack_zips(verbose=verbose)
    remove_tmp_dir()
    if verbose:
        print("All done. Have fun!")
