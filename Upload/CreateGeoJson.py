import os
import json
import glob
from datetime import datetime, timezone


def process_store_polygons(store_name, pincodes_str, polygons_path="../Polygons"):
    """
    Process polygon files for a store and pincodes, creating new JSON files.

    Args:
    store_name (str): Store code like "BCE"
    pincodes_str (str): Comma-separated pincodes like "711205, 711206"
    polygons_path (str): Path to polygons directory
    """
    # Parse pincodes
    pincodes = [pin.strip() for pin in pincodes_str.split(',')]

    # Find matching files using glob pattern
    pattern = os.path.join(polygons_path, f"1MG_{store_name}_*_*.geojson")
    matching_files = glob.glob(pattern)

    if not matching_files:
        print(f"No polygon files found for store {store_name} in {polygons_path}")
        return

    print(f"Found {len(matching_files)} polygon files: {matching_files}")

    for file_path in matching_files:
        try:
            # Load original GeoJSON
            with open(file_path, 'r') as f:
                original_data = json.load(f)

            # Extract filename without extension
            file_name = os.path.basename(file_path).replace('.geojson', '')

            # Use first feature's geometry (or modify logic as needed)
            if not original_data.get('features') or not original_data['features']:
                print(f"Skipping {file_path}: No features found")
                continue

            geometry = original_data['features'][0]['geometry']

            # Create UTC timestamp in Z format
            utc_timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

            # Create new structure
            new_data = {
                "name": file_name,
                "business_line": "PHARMACY",
                "description": "Testing",
                "geojson": {
                    "type": "Feature",
                    "properties": {
                        "key": utc_timestamp,  # Now in Z format: 2025-12-29T08:00:24.544Z
                        "name": file_name,
                        "focused": False
                    },
                    "geometry": geometry
                },
                "status": "active",
                "layers": [
                    {
                        "key": "pincode",
                        "value": pincode
                    }
                    for pincode in pincodes
                ],
                "user_id": "munish.thakral@1mg.com"
            }

            # Save new file
            output_file = os.path.join("Polygons", file_name + ".geojson")
            with open(output_file, 'w') as f:
                json.dump(new_data, f, indent=4)

            print(f"Created: {output_file} with timestamp: {utc_timestamp}")

        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

store = "TPR"
pincodes = "700063, 700104, 700061, 700008"
process_store_polygons(store, pincodes)