import os
import requests
import json

API_KEY = "AIzaSyCowToq63AeA_L_Iq2XJerHLnWfEndj6IQ"


def main():
    with open("schipholler/destinations_data/destinations.json") as f:
        destinations = json.load(f)

    print(len(destinations))

    new_destinations = []
    for i, destination in enumerate(destinations):
        city = destination["city"]
        if not city:
            continue
        print(i, city)
        api_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={API_KEY}"

        response = requests.get(
            api_url,
        )

        if response.status_code == requests.codes.ok:
            result = response.json()["results"]

            if len(result) > 0:
                location = result[0]["geometry"]["location"]
                longitude, latitude = location["lng"], location["lat"]

                new_dest = {
                    "city": destination["city"],
                    "country": destination["country"],
                    "iata": destination["iata"],
                    "publicName": destination["publicName"],
                    "longitude": longitude,
                    "latitude": latitude,
                }
                new_destinations.append(new_dest)

        else:
            print("Error:", response.status_code, response.text)

    folder_path = "schipholler/destinations_data"
    file_name = "destinations_with_coords.json"
    # csv_file_name = "destinations.csv"

    file_path = os.path.join(folder_path, file_name)
    # csv_file_path = os.path.join(folder_path, csv_file_name)

    # Make sure the folder exists, create it if necessary
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(new_destinations, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()


{
    "results": [
        {
            "address_components": [
                {
                    "long_name": "Aalborg",
                    "short_name": "Aalborg",
                    "types": ["locality", "political"],
                },
                {
                    "long_name": "Denmark",
                    "short_name": "DK",
                    "types": ["country", "political"],
                },
            ],
            "formatted_address": "Aalborg, Denmark",
            "geometry": {
                "bounds": {
                    "northeast": {"lat": 57.07916789999999, "lng": 10.0656796},
                    "southwest": {"lat": 56.9745056, "lng": 9.7498684},
                },
                "location": {"lat": 57.0488195, "lng": 9.921747},
                "location_type": "APPROXIMATE",
                "viewport": {
                    "northeast": {"lat": 57.07916789999999, "lng": 10.0656796},
                    "southwest": {"lat": 56.9745056, "lng": 9.7498684},
                },
            },
            "place_id": "ChIJDT3fX7IzSUYRwybsLmq0sU4",
            "types": ["locality", "political"],
        }
    ],
    "status": "OK",
}
