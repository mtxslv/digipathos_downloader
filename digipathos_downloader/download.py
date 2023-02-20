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

def download_zips(zips_tbl: list, 
                  tmp_dir: str = '.',                                  
                  verbose: bool = True,
                  base_url: str = "https://www.digipathos-rep.cnptia.embrapa.br"):
    
    """Iterates over the samples metadata and download them.

    Args:
        zips_tbl (list): the samples metadata (i.e., generated by fetch_zips_table).
        tmp_dir (str): the directory where your zipped files are (i.e., tmp folder). Defaults to '.'.
        verbose (bool): notify the user about the progress. Default to True
        base_url (str): digipathos base url. Defaults to "https://www.digipathos-rep.cnptia.embrapa.br".
    
    Returns:
        not_downloaded (list): the failed downloads' urls. None if successful.
    """              
    not_downloaded = []
    for index, remote_zip_info in enumerate(zips_tbl):
        if verbose:
            print(f"Downloading ZIP-file {index+1}/{len(zips_tbl)}...")
        fail_download = download_zip(remote_zip_info["bsLink"], 
                                     remote_zip_info["name"],
                                     tmp_dir,
                                     base_url)
        if fail_download != None:
            not_downloaded.append(fail_download)
    if len(not_downloaded) > 0:
        return not_downloaded

def validate_downloads(n_zips: int, 
                       dir: str, 
                       verbose: bool = True) -> tuple:
                       
    """Validate if the samples were successfully downloaded. The number of files found in the repository is returned.
       Files with 0 bytes of size have their names returned. 

    Args:
        n_zips (int): the expected number of zipped files.
        dir (float): the directory where your zipped files are (i.e., tmp folder).
        verbose (bool): notify the user about the progress. Defaults to True.

    Returns:
        (tuple): the number of files in directory (n_zips_in_tmp) and a list of files with size of 0 bytes (zero_size_files).
    """                   
    tmp_dir = dir + '/'   
    zero_size_files = []                  
    if verbose:
        print("Validating downloads...")
    n_zips_in_tmp = len([name for name in os.listdir(tmp_dir)])
    if n_zips_in_tmp != n_zips:
        print(f"WARNING: Number of ZIP-files in {tmp_dir} is not the same as retrieved from the EMPRABA website.\n"
              f"Expected number of ZIP-files: {n_zips}. ZIP-files found in directory: {n_zips_in_tmp}.")
    for filename in os.listdir(tmp_dir):
        if os.path.getsize(tmp_dir + filename) == 0:
            zero_size_files.append(tmp_dir + filename)
            print(f"WARNING: ZIP-file {filename} has a size of 0 bytes.")
    return n_zips_in_tmp, zero_size_files

def unpack_zip(filename: str,
               data_dir: str,
               tmp_dir: str):
    """Extracts a file to a given folder.

    Args:
        filename (str): name of the zip file to be extracted.
        data_dir (str): path for the folder where the files will be extracted to.
        tmp_dir (str): path for zip file origin.

    Returns:
        file_to_be_extracted (str): path for the file whose extraction failed. Not returned if extraction is succesful.
    """
    class_dir = data_dir + "/" + filename[:-4] # DATA_DIR = "/plant-disease-db"
    try:
        create_dir(class_dir)
        file_to_be_extracted = tmp_dir + '/' + filename
        with zipfile.ZipFile(file_to_be_extracted, mode="r") as zip_contents: # TMP_DIR = "/plant-disease-db/tmp"
            zip_contents.extractall(class_dir)
    except IOError as e:
        print(f"{e}\nSkipping unpacking of {filename}")
        return file_to_be_extracted

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
