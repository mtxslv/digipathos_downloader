# Welcome! 👋👋

`digipathos_downloader` is a Python package for downloading [Embrapa's Digipathos Dataset](https://www.digipathos-rep.cnptia.embrapa.br/). In case you didn't know, the dataset contains images and descriptions of several vegetables diseases. The project is based on [george-un's](https://github.com/georg-un/digipathos-plant-disease-img-db-downloader). Kudos to him! Without his implemented logic, surely this project would not be possible.

# 🤔 What does this lib do? 🤔

This lib is capable of fetching the original zipped files paths, and download and unzip them.

Available functions:
- `create_basic_folder_structure`: creates a folder for the dataset (*dataset_dir/*) and another one for the downloads (_tmp/_). It calls `create_dir` to do it.
- `fetch_zips_table`: fetches metadata from the files.
- `download_zips`: uses the metadata to download the files themselves. Calls `download_zip` several times.
- `validate_downloads`: validates the scheduled amount of downloads were done correctly.
- `unpack_zips`: unzips the files in the _tmp/_ folder. Calls `unpack_zip` several times.
- `remove_tmp_dir`: deletes the downloads folder.
- `get_dataset`: orchestrates the download end-to-end.

Not available:
- ~~`main`~~ (currently broken and untested): called during CLI. Inherited from the original project.

**Currently, CLI use is not available. The original project was meant to be called using CLI. Since this one aims to be employed in code, There is no plan to add CLI use.**

#  👩‍💻 How to install? 👨‍💻

In order to install the lib in a Linux based system, run:

```shell
pip install git+https://github.com/mtxslv/digipathos_downloader
```

If you have Poetry available in your system, you can do:

```shell
poetry add git+https://github.com/mtxslv/digipathos_downloader
```

# It seems amazing 🤩! But I have no idea how to start 😓. What should I do? 🧐

Once you have downloaded the project, you can get the dataset using:

```python
from pathlib import path
from digipathos_downloader import download

my_folder = Path(__name__).absolute().parent # this is the folder you are in
dataset_dir = my_folder / 'dataset_dir' # here is where the unzipped files will be 
tmp_dir = my_folder / 'tmp' # this folder is used during installation and deleted once it is over

# get the dataset
download.get_dataset(str(dataset_dir),
                     str(tmp_dir))
```

This must be suficient to download the dataset to ```dataset_dir```.

More references regarding the use of the other functions are found in the [tests folder](./tests/) and in the functions docstrings.

# ✍🏼 Some Last Words... ✍🏼

Your feedback is much appreciated 🫂.

If you developed something interesting using the lib, please consider showing the world. Don't be shy! You can tag [my Linkedin account](https://www.linkedin.com/in/mateus-assis-013a46140/) or [my Github](https://github.com/mtxslv/).

If you find any bugs, or unexpected behaviour, submit an issue in the project. I'll answer it ASAP 😉

#
**_That said, happy coding!_**