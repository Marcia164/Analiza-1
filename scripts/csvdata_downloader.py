import datetime as dt
import requests
import os
import pandas as pd
import shutil
import filefinder

# Actual timestamp

print("Generating timestamp for the filename...")
ts = dt.datetime.now().strftime("%Y%m%d_%H-%M")

# Create a filename with the timestamp

csv_filename = f"../data/smog_{ts}.csv"
json_filename = f"../data/smog_{ts}.json"
print(f"Created filename: {json_filename}, {csv_filename}")
    
# Function cleaning json file and validating it as csv

def json_cleaner(json_filename, csv_filename):
    print("Starting file cleaning.")

    # Transfer json to csv for easier cleaning

    df_json = pd.read_json(json_filename, encoding='utf-8-sig')
    df_json.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    df_json = pd.read_csv(csv_filename, encoding='utf-8-sig')
    print("Converting downloaded json to csv file.")

    # Drop unnecessary columns

    df_json = df_json.drop(columns=['it_has_next_page', 'pages_total'])
    print("Removing unnecessary columns.")

    # List of columns in file

    headlist = [
        "\'name\': ",
        " \'street\':",
        " \'post_code\':",
        " \'city\':",
        " \'longitude\':",
        " \'latitude\':",
        " \"humidity_avg\":",
        " \'pressure_avg\':",
        " \'temperature_avg\':",
        " \'pm10_avg\':", 
        " \'pm25_avg\':",
        " \'timestamp\':"
        ]

    # Remove column names from inside of file

    for x in df_json['smog_data']:
        for y in headlist:
            df_json['smog_data'] = df_json['smog_data'].str.replace(y, "")
    print("Cleaning column names in the file.")

    # Clear basic unnecessary chars

    for x in df_json['smog_data']:    
        df_json['smog_data'] = df_json['smog_data'].str.replace("{\'school\': {", "")
        df_json['smog_data'] = df_json['smog_data'].str.replace("}, \'data\': {", ", ")
        df_json['smog_data'] = df_json['smog_data'].str.replace("}", "")
        df_json['smog_data'] = df_json['smog_data'].str.replace("\\t", "")
        df_json['smog_data'] = df_json['smog_data'].str.replace("\\r", "")
        df_json['smog_data'] = df_json['smog_data'].str.replace("\\n", "")
        df_json['smog_data'] = df_json['smog_data'].str.replace(" humidity_avg:", "")
        df_json['smog_data'] = df_json['smog_data'].str.replace("None", "")
        df_json['smog_data'] = df_json['smog_data'].str.replace("\'", "")
        df_json['smog_data'] = df_json['smog_data'].str.replace(",,", "")
        df_json['smog_data'] = df_json['smog_data'].str.replace("\\xa", "")
    print("Cleaning basic unnecessary characters.")


    # Save current changes to the temp file

    output = "../temp/smog_jsonclean2.csv"
    input = "../temp/smog_jsonclean.csv"

    df_json.to_csv(input, index=False, encoding='utf-8-sig')
    df_json.to_csv(output, index=False, encoding='utf-8-sig')
    print("Saved temporary files.")

    # Remove "\"" characters fom file

    with open(input, 'r', encoding='utf-8-sig') as f:
        with open(output,'w', encoding='utf-8-sig') as ff:
            ff.write(f.read().replace("\"", ""))
    print("Removing \" characters from csv file.")

    # Create column names at the top of csv file, add 2 temporary backup columns

    header = "\"NAME\",\"STREET\",\"POST_CODE\",\"CITY\",\"LONGITUDE\",\"LATITUDE\",\"HUMIDITY_AVG\",\"PRESSURE_AVG\",\"TEMPERATURE_AVG\",\"PM10_AVG\",\"PM25_AVG\",\"TIMESTAMP\",\"ERROR1\""

    with open(output, 'r', encoding='utf-8-sig') as f:
        with open(csv_filename,'w', encoding='utf-8-sig') as ff:
            ff.write(f.read().replace("smog_data", header))
    print("Adding column headers + backup error column.")

    # Set data frame with column headers
    
    df_json = pd.read_csv(csv_filename, encoding='utf-8-sig')
    
    # Clean columns with coma in "NAME" column
    
    print("Removing coma characters from \"NAME\" column.")
    df_json['ERROR1'] = pd.to_datetime(df_json['ERROR1'], errors='coerce')
    with open(csv_filename, 'r', encoding='utf-8-sig') as f:
        with open(output,'w', encoding='utf-8-sig') as ff:
            lines = f.readlines()
            ff.write(lines[0])
            for x, y in df_json['ERROR1'].items():
                x += 1
                if type(y) != type(pd.NaT):
                    ff.write(lines[x].replace(",", '', 1))
                else:
                    ff.write(lines[x])
    
    # Set clean data frame
    
    df_json = pd.read_csv(output, encoding='utf-8-sig')

    # Removing temporary error column
    
    df_json = df_json.drop(columns=['ERROR1'])
    print("Removing error column.")
    
    # Saving file to csv
    
    df_json.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    
    # Check if file exists and provide a message
    
    if os.path.exists(csv_filename):
        print(f"Transferred json to the csv file.")
        print(f"File saved: {csv_filename}")
    else:
        print("Failed to transfer into csv file.")
        
    print("Cleaning successful.")
            
    # Remove json file transferred to csv
    
    if os.path.exists(json_filename): 
        os.remove(json_filename)
        print(f"File '{json_filename}' deleted successfully.")
    else: 
        print(f"File '{json_filename}' not found.")

# Define function for downloading json file:

def file_downloader():
    # Link to the data file

    json_link = "https://public-esa.ose.gov.pl/api/v1/smog"
    #csv_link = "https://public-esa.ose.gov.pl/api/v1/smog/csv"

    #  Download the  file and save it with the timestamp in the filename

    print(f"Downloading the json file from {json_link}...")
    response = requests.get(json_link)
    with open(json_filename, 'wb') as file:
        file.write(response.content)

    # Check if the file was downloaded successfully. 

    if os.path.exists(json_filename):
        print(f"Downloaded and saved the json file")
        print(f"File saved: {json_filename}")
    else:
        print("Failed to download the json file.")


# Download file every set amount of time set number times and  merge with earlier downloaded file

def file_merger():
    merged_datafiles = '../data/smog_merged.csv'
        
    # Provide datafile list and create empty merger file
    
    finder = filefinder.Finder('../data/', 'smog_%(Y)%(m)%(d)_%(H)-%(M).csv')
    datafile_list = finder.get_files()
    print(f"Datafile list: {datafile_list}")
    if not os.path.exists(merged_datafiles):
        with open(merged_datafiles, "x") as file:
            file.write("")
            print("Empty file for data merging created.")
    elif os.path.exists(merged_datafiles):
        shutil.copy(merged_datafiles, '../temp/merged_files_backup.csv')
        os.remove(merged_datafiles)
        with open(merged_datafiles, "x") as file:
            file.write("")
            print("Earlier merging file deleted and new empty file for data merging created.")

    # Merge new files into base file

    datafiles = pd.DataFrame()

    for n in datafile_list:
        df1 = pd.read_csv(n, encoding='utf-8-sig')
        datafiles = pd.concat([datafiles, df1], ignore_index=True)
    print("Merged all files from datafile list.")

    datafiles.to_csv(merged_datafiles, index=False, encoding='utf-8-sig')
    print("Saved merged files to csv file.")

# Download json file

file_downloader()

# If downloaded file exists, perform cleaning on it and turn into csv file.

json_cleaner(json_filename, csv_filename)

# Get all downloaded files from datafile list and merge them into one file.

file_merger()