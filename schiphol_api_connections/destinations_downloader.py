import json
import os
import re

import pandas as pd
import requests

APP_KEY = "9c4c29278420898f1a69c056f663cdec"
APP_ID = "d68e0bbe"

url = "https://api.schiphol.nl/public-flights/destinations"

payload = {}
files = {}
headers = {
    "ResourceVersion": "v4",
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "Accept": "application/json",
    "Cookie": "7182e1354ced9d56d758a37dabb724b0=690ae31976eaeae3fc234660a32092a1",
}


def get_all_destinations(url, jsons=[]):
    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    print(response.status_code)

    jsons.append(response.json())

    match = re.search(r'<([^>]+)>;\s*rel="next"', response.headers["link"])

    if match:
        next_url = match.group(1)
        get_all_destinations(next_url)
    else:
        print("No URL found for 'rel=\"next\"'")
        match = re.search(r'<([^>]+)>;\s*rel="last"', response.headers["link"])
        next_url = match.group(1)
        response = requests.request(
            "GET", url, headers=headers, data=payload, files=files
        )
        print(response.status_code)
        jsons.append(response.json())

    return jsons


def main():
    jsons = get_all_destinations(url)

    data = [file["destinations"] for file in jsons]
    flat_data = [item for sublist in data for item in sublist]

    data_processed = [
        {
            "city": destination["city"],
            "country": destination["country"],
            "iata": destination["iata"],
            "publicName": destination["publicName"]["english"],
        }
        for destination in flat_data
        if destination["iata"]
    ]

    folder_path = "schipholler/destinations_data"
    file_name = "destinations.json"
    # csv_file_name = "destinations.csv"

    file_path = os.path.join(folder_path, file_name)
    # csv_file_path = os.path.join(folder_path, csv_file_name)

    # Make sure the folder exists, create it if necessary
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(data_processed, f, ensure_ascii=False, indent=4)


def change_destinations_to_csv():
    folder_path = "schiphol_api_connections/destinations_data"
    file_name = "destinations_with_coords.json"
    csv_file_name = "destinations_with_coords.csv"

    file_path = os.path.join(folder_path, file_name)
    csv_file_path = os.path.join(folder_path, csv_file_name)

    with open(file_path, "r") as f:
        data = pd.read_json(f)

    keys = data[0].keys()
    print(keys)

    data.to_csv(csv_file_path)


if __name__ == "__main__":
    change_destinations_to_csv()
