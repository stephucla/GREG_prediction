import os
import pandas as pd
import csv
import re
# import sys
# directory_path = str(sys.argv[1])

# Using BERT annotations
def count_locations(text_file):
    pattern = re.compile(r"([\s])?(INT\.|INT,|INT|EXT\.|EXT,|EXT|Interior:|Exterior:)( [\w\s]+: | |-| - )([\w\s'’]+)(-| -|,| \()?")
    unique_locations = set()
    with open(text_file, "r", encoding="utf8") as file:
        lines = file.readlines()
        for line in lines:
            match = pattern.search(line)
            if match:
                location = match.group(4).strip()
                unique_locations.add(location.lower())
    # print(unique_locations)
    return len(unique_locations)

# Return dataframe containing imdbid and number of locations
def get_num_locations_df(directory_path):
    file_names = os.listdir(directory_path)
    files = []
    for file_name in file_names:
        file = str(directory_path + "\\" + file_name)
        files.append(file)
    df = pd.DataFrame()
    for file in files:
        print("Looking at file: ", file)
        movie_title = file.replace(directory_path + "\\", "").split("_")[0]
        movie_id = int(file.replace(directory_path+"\\", "").split("_")[1])
        num_of_locations = count_locations(file)
        df = df._append({"imdbid": movie_id, "title": movie_title, "number of locations": num_of_locations}, ignore_index=True)
    return df

# Creates num_of_locations.csv file containing imdbid and number of locations
def get_num_locations_csv(directory_path):
    file_names = os.listdir(directory_path)
    files = []
    for file_name in file_names:
        file = str(directory_path + "\\" + file_name)
        files.append(file)

    with open("num_of_locations.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        field = ["imdbid", "number of locations"]
        writer.writerow(field)

        for file in files:
            print("Looking at file: ", file)
            movie_id = int(file.replace(directory_path + "\\", "").split("_")[1].split(".")[0])
            num_of_locations = count_locations(file)
            writer.writerow([movie_id, num_of_locations])

if __name__ == '__main__':
    directory_path = input("Enter directory path: ")
    # df = get_num_locations_df(directory_path) # get dataframe
    # print(df)
    get_num_locations_csv(directory_path) # or get csv file