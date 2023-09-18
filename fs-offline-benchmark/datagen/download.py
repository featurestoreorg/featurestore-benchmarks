import os
import requests

years = [
    "2011",
    "2012",
    "2013",
    "2014",
    "2015",
    "2016",
    "2017",
    "2018",
    "2019",
    "2020",
    "2021",
]

# Sample url (cloudfront may change over time):
# https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2017-01.parquet


base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
file_base = "yellow_tripdata_"
file_ending = ".parquet"

for year in years:
    year_dir_path = os.getcwd() + "/" + year
    if not os.path.exists(year_dir_path):
        os.makedirs(year_dir_path)
    print(f"Downloading data for {year} to {year_dir_path}")
    for month in range(1, 13):  # 1 - 12
        if month < 10:
            month = "0" + str(month)
        file_name = file_base + year + "-" + str(month) + file_ending
        download_url = base_url + file_name
        file_write_path = year_dir_path + "/" + file_name
        if not os.path.exists(file_write_path):
            print(
                f"File {file_name} not found in local path provided... trying download now..."
            )
            req = requests.get(download_url)
            open(file_write_path, "wb").write(req.content)
        else:
            print(f"File {file_name} already exists. Skipping download.")
