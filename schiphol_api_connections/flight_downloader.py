import requests
import re
import json
import sys
import os
import csv


APP_KEY = "9c4c29278420898f1a69c056f663cdec"
APP_ID = "d68e0bbe"

url = "https://api.schiphol.nl/public-flights/flights"

payload = {}
files = {}
headers = {
    "ResourceVersion": "v4",
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "Accept": "application/json",
    "Cookie": "7182e1354ced9d56d758a37dabb724b0=690ae31976eaeae3fc234660a32092a1",
}


def request_one_day(url, jsons=[]):
    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    print(response.status_code)

    jsons.append(response.json())

    match = re.search(r'<([^>]+)>;\s*rel="next"', response.headers["link"])

    if match:
        next_url = match.group(1)
        request_one_day(next_url)
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
    print(sys.path)

    date = "2023-10-04"

    url_specific = f"{url}?scheduleDate={date}"

    jsons = request_one_day(url_specific)

    data = [file["flights"] for file in jsons]
    flat_data = [item for sublist in data for item in sublist]

    folder_path = "schipholler/flight_data"
    file_name = f"{date}.json"
    csv_file_name = f"{date}.csv"

    file_path = os.path.join(folder_path, file_name)
    csv_file_path = os.path.join(folder_path, csv_file_name)

    # Make sure the folder exists, create it if necessary
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(flat_data, f, ensure_ascii=False, indent=4)

    keys = flat_data[0].keys()

    with open(csv_file_path, "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(flat_data)


if __name__ == "__main__":
    main()
