# Intro

This fork makes [georg-un's installer](https://github.com/georg-un/digipathos-plant-disease-img-db-downloader) installable by pip or poetry. That is, it is not necessary to git-clone the repo. Just ```poetry add``` it and that is it..

**original docs below**

# Digipathos Plant Disease Image Database Downloader
This project is a downloader for the plant disease image database provided by EMBRAPA (Brazilian Agricultural Research Corporation). Further information on the database can be found in [this](https://doi.org/10.1016/j.biosystemseng.2018.05.013) paper.

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/70ab11e8a9284cac8abdac662facb22f)](https://www.codacy.com/app/georg-un/embrapa-plant-disease-img-db-downloader?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=georg-un/embrapa-plant-disease-img-db-downloader&amp;utm_campaign=Badge_Grade)

## Requirements
You will need **python 3.6 or higher** installed.
Additionally, you will need the python module *requests*. If you haven't already installed it, install it with `pip install requests`.

## Installation
With [git](https://git-scm.com/downloads) installed, you can install the downloader with:
```shell
git clone https://github.com/georg-un/digipathos-plant-disease-img-db-downloader
cd digipathos-plant-disease-img-db-downloader
```

## Usage
To use the downloader, open a terminal in the project folder and run the following command:
```shell
python3.6 run.py
```

**Note:** You can tell the script to download only original or cropped images.<br/>
To download only original images use the command `python3.6 run.py original`.<br/>
To download only cropped images use the command `python3.6 run.py cropped`.
