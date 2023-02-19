# UNDERSTANDING THE CONTEXT

A lil' bit of context: so far, I added everything in poetry, but it is not working yet. I want to find out why.

My first step is the most obvious one: let's try to understand how the process work. This readme file contains an explanation of what I've discovered.

## EXECUTING THE [ORIGINAL PROJECT](https://github.com/georg-un/digipathos-plant-disease-img-db-downloader)

### RUN PYTHON IN SHELL

In order to execute the code (original project), we run: 

```shell
python3.6 run.py
```

This will call the [run.py](./run.py) script

### RUN.PY

The _run.py_ script does the following:
1. check if the user passed any more flags. If not, the filter name is "all".
2. Run the main function located at the [download.py script](./download.py)

### DOWNLOAD.PY

1. The main function calls a lot of functions defined within the same file. These will be explained in the following topics. But here they are (listing for display purposes):
    1. create basic folder structure
    2. fetch zips table
    3. download zips
    4. validate downloads
    5. unpack zips
    6. remove temporary directory
    7. Notify the user the download is over (if specified)
2. `create_basic_folder_structure`: this function creates two directories: the DATA_DIR (_./plant-disease-db/_) and the TMP_DIR (_./tmp/_). If an error occurs, it is raised and notified. This function calls `create_dir` function, which directly creates the folder in a given path.
3. `fetch_zips_table`: this function fetches the available files to be downloaded through a get request. Query parameters (offset and limit) as a dictionary to the _requests.get()_ function. The *name_filter* parameter lets the user choose which images will be returned (original, cropped, or both).
4. `download_zips`: this function iterates over the fetched information returned by the previous and for each piece it downloads the zipped images. The download function is `download_zip`. It tries thrice to get the content from the url and then writes it locally. If anything goes wrong, and exception is thrown and the user is notified.
5. `validate_downloads`: this function validates if all elements were downloaded and their sizes are non-zero.
6. `unpack_zips`: tries to unzip the files by iterating over the names of the downloaded files in the _/tmp/_ folder. The function `unpack_zip` does unzip and, if something goes wrong, the file is skipped. The unzipped file is moved to the DATA_DIR (_./plant-disease-db/_). 
7. `remove_tmp_dir`: deletes the TMP_DIR (_./tmp/_). 


# TURNING THE PROJECT INTO A LIB

## FOLDER STUFF
The first step is to move all necessary code into a proper folder. Thus, the files:
- `download.py`;
- `run.py`; and
- `setup_ckecks.py`

are moved into `./digipathos_downloader/`. An `__init__.py` is added too

Create tests for the module and add them in the `./test` folder. Notice [the order the dependencies are called](https://code.visualstudio.com/docs/python/editing):
- native libs
- installed libs
- your lib

And they are called alphabetically

## ADD TEST

Even though the original code was working perfectly, it was developed to be called through command-line. In order to use it on a pipeline it would be necessary to refactor it. Necessary modifications:
- The global variables (BASE_URL, LIST_URL, WORKING_DIR, DATA_DIR, and TMP_DIR) must become local (function arguments);
- The functions must be more customizable. For instance, it is necessary to change the target directory to download the samples (just in case we need to test something). It is also necessary to make the urls changeable (as function arguments), just in case the website changes in the future;
- Failed downloads must be somewhat registered as code (not just notified). Thus, it is necessary to make the functions return the broken urls;
- Add docstrings to ease understanding;

All this context further reaffirm the need for tests (something originally missing).