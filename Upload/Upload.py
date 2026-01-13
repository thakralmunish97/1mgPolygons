import os
import glob
import json
import requests
from pathlib import Path

def upload_polygons():
    # API endpoint and headers
    url = "https://unifiedadmin.1mg.com/vendor_service_api/v1/polygons"
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': 'e4d5c5f2-126a-46b4-b5a8-d65a0b728953',
        'content-type': 'application/json',
        'origin': 'https://unifiedadmin.1mg.com',
        'priority': 'u=1, i',
        'referer': 'https://unifiedadmin.1mg.com/vendor-hub/polygon-manager/polygons/create',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin'
    }

    polygons_dir = Path("Polygons")
    geojson_files = list(polygons_dir.glob("*.geojson"))

    print(f"Found {len(geojson_files)} .geojson files in Polygons directory")

    for geojson_file in geojson_files:
        try:
            # Read GeoJSON file
            with open(geojson_file, 'r') as f:
                geojson_data = json.load(f)

            # POST request
            response = requests.post(url, headers=headers, json=geojson_data)

            if response.status_code == 201:
                print(f"Done: {geojson_file.name}")
            else:
                print(f"Failed {geojson_file.name}: Status {response.status_code}")

        except Exception as e:
            print(f"Error processing {geojson_file.name}: {str(e)}")

    # Clear the directory after processing all files
    for geojson_file in geojson_files:
        geojson_file.unlink()

    print("Polygons directory cleared")

upload_polygons()