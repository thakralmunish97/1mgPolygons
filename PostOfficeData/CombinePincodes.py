import geopandas as gpd
from pathlib import Path
import json


def combine_geojson_polygons(directory_path, polygon_names, output_file):
    """
    Combines multiple GeoJSON polygon files into a single GeoJSON FeatureCollection.

    Args:
        directory_path (str): Path to directory containing GeoJSON files
        polygon_names (list): List of polygon file names (without .geojson extension)
        output_file (str): Output file path for combined GeoJSON
    """
    directory = Path(directory_path)
    combined_features = []

    for name in polygon_names:
        file_path = directory / f"{name}.geojson"
        if not file_path.exists():
            print(f"Warning: File {file_path} not found, skipping.")
            continue

        with open(file_path, 'r') as f:
            data = json.load(f)

        # Handle both Feature and FeatureCollection inputs
        if data['type'] == 'FeatureCollection':
            features = data['features']
        elif data['type'] == 'Feature':
            features = [data]
        else:
            print(f"Warning: {name}.geojson is not a valid Feature or FeatureCollection, skipping.")
            continue

        combined_features.extend(features)

    # Create output FeatureCollection
    output_geojson = {
        'type': 'FeatureCollection',
        'features': combined_features
    }

    with open(output_file, 'w') as f:
        json.dump(output_geojson, f, indent=2)

    print(f"Combined {len(combined_features)} features from {len(polygon_names)} files into {output_file}")


def combineIntoOnePolygon(filename):
    """
    Combines all polygons in a GeoJSON file into a single polygon and saves as new GeoJSON.

    Parameters:
    filename (str): Path to input GeoJSON file.

    Returns:
    str: Path to the output combined GeoJSON file.
    """
    input_path = Path(filename)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {filename}")

    # Read the GeoJSON file
    gdf = gpd.read_file(str(input_path))  # Handles FeatureCollection automatically [web:16][web:19]

    # Ensure it's polygons
    if gdf.geometry.type.str.contains('Polygon|MultiPolygon', na=False).all() == False:
        raise ValueError("GeoDataFrame must contain only Polygon or MultiPolygon geometries.")

    # Union all geometries into one
    single_geom = gdf.geometry.unary_union  # Efficient union of multiple polygons [web:3][web:6]

    # Create new GeoDataFrame with single feature (no properties or empty dict)
    combined_gdf = gpd.GeoDataFrame([{}], geometry=[single_geom], crs=gdf.crs)

    # Output path
    output_path = input_path.with_name(input_path.stem).with_suffix('.geojson')

    # Save as GeoJSON FeatureCollection with one feature
    combined_gdf.to_file(str(output_path), driver='GeoJSON')  # Preserves CRS and geometry [web:16]

    return str(output_path)

# Example usage:
FileName = "Hyderabad.geojson"
polygon_names = ["500051","500073","500090","500030","500098","500052","500081","500063","500054","500045","500036","500027","500018","500009","500048","500096","500050","500032","500005","500100","500074","500047","500038","500029","500010","500001","502319","500028","500076","500014","500016","500035","500062","500008","500034","500080","500070","500044","501401","500079","500060","500033","501218","500057","500039","500020","500015","500095","500086","500077","500068","500059","500040","500013","500091","500082","500064","500053","500022","500055","500007","500006","500097"]
combine_geojson_polygons("../Pincodes", polygon_names, "../City/" + FileName)
combineIntoOnePolygon("../City/" + FileName)

