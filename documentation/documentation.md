# Project Documentation

This is a simple markdown-style documentation file. It gives a short overview of the main files in this project and explains how they work together.

## Overview

- This document describes the basic structure and purpose of the files in the project.
- It is not a full reference guide, but a demo version of documentation for quick understanding.

## Files and Purpose 

  - .gitignore - a file which states, which files and directories shouldn't be pushed (or sent away) to git servers.
  - README - a file with basic description of the project.
  - licenses - basic license files downloaded with database files and made when this project started.

### Data

  * smog_merged.csv - a file which contains all merged files having filename like "smog_%(Y)%(m)%(d)_%(H)-%(M).csv" into one file.
  * smog_%(Y)%(m)%(d)_%(H)-%(M).csv - a file downloaded at a time saved in the timestamp.
  * mapa_szkol%(Y)%(m)%(d)_%(H)-%(M) - an HTML document showing placement of schools from which the data was taken. The color of pinpoint shows, whether the PM values are in norm or exceed it.

### Scripts

  1. csvdata_downloader - a script for downloading current csv data file from data provider and saving it in "data" directory. For executing should be put in scripts directory and just run. When run, it creates an actual timestamp so a user knows from which hour the data is collected. Then a name "smog + timestamp" is created and file is saved (and there is an information about success or failure). * [04.07.2026] - changed, so firstly is downloaded json file, and then it is changed to csv file type. It is also cleaned of wrong characters. First column value is cleaned from commas if any occur. When downloading file with file merger on, the downloaded file is automatically merged into "./data/smog_merged.csv" with all csv files which have a filename like "smog_%(Y)%(m)%(d)_%(H)-%(M).csv" and are in data directory.

  2. smog_raw - jupyter script which manages first, basic data wrangling on smog_raw.csv data file. Saves changed file in "tests" directory, with added timestamp. Adds an area column to the data frame and fills it with province names based on postal code. Removes "-" from post code so it can be read as an integer. Checks, if every city is in the Poland area based on max latitude and longitude (N, S, E and W point), and returns, how many are outside these points.

  3. smog_report_generator - jupyter file to run smog_raw and get reports from executed scripts as pdf and html files.

### Scripts_different

  - [x] Backupper - a script to backup all repo data in a directory one level higher. To do this, just put a "backupper.py"  file in any directory (preferably "scripts_different") in repository and run it. It will make a "backup" directory one level higher, make inside a directory named "analiza + actual timestamp" and copy whole repo there.

### Reports

  - smog_html%(Y)%(m)%(d)_%(H)-%(M).html - an HTML report file generated with smog_raw.ipynb based on data from smog_merged.csv
  - smog_pdf%(Y)%(m)%(d)_%(H)-%(M).pdf - a PDF report file generated with smog_raw.ipynb based on data from smog_merged.csv

### Temp

  - smog_jsonclean*.csv - a file made to backup cleaning json file process when transferring to csv.
  - merged_files_backup.csv - a file made, when creating new file merged from all other csv datafiles.

### Tests

  - smog_raport_raw%(Y)%(m)%(d)_%(H)-%(M).csv - final raw csv data raport, generated after all cleaning, sorting, column adding etc.

## How the Files Work Together

  First, the smog_report_generator.ipynb should be run. It then runs smog_raw.ipynb, which is the main script to get report done and runs all packets needed to run the report generator. Then, csvdata_downloader.py is run, and it downloads last data into csv file, cleans from different errors and merges it with all other files which were downloaded earlier into smog_merged file. Next, merged files are proceeded and based on generated data there is generated final report in reports directory. Also, there is generated HTML file which visualises data on map.

## Dependencies

  To properly run, the pip should have installed some packets. Here is list of them:
- pandas
- numpy
- datetime
- missingno
- seaborn
- matplotlib
- skimpy
- IPython
- folium
- ipywidgets
- filefinder
- shutil
- requests
- nbconvert
- nbformat
  Also, to generate a pdf file, the latex (https://miktex.org/download) and pandoc (https://pandoc.org/installing.html) packets needed.

## Notes

- This document is intended as a simple, high-level guide.
- For more detailed explanations, inspect each file directly.