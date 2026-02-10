import json
from copy import deepcopy

def multipolygon_to_polygons_featurecollection(input_path, output_path):
    # Load original GeoJSON
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    features = data.get("features", [])
    out_features = []

    for feat in features:
        geom = feat.get("geometry", {})
        gtype = geom.get("type")
        coords = geom.get("coordinates", [])

        # If it's already a Polygon, keep as is
        if gtype == "Polygon":
            out_features.append(feat)
            continue

        # If it's a MultiPolygon, split into multiple Polygon features
        if gtype == "MultiPolygon":
            for poly_coords in coords:
                new_feat = deepcopy(feat)
                new_feat["geometry"] = {
                    "type": "Polygon",
                    "coordinates": poly_coords
                }
                out_features.append(new_feat)
        else:
            # Optional: keep other geometry types untouched
            out_features.append(feat)

    # Build new FeatureCollection
    out = {
        "type": "FeatureCollection",
        "features": out_features
    }

    # Preserve optional top-level keys like name, crs if present
    for key in ["name", "crs"]:
        if key in data:
            out[key] = data[key]

    # Write to file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)


multipolygon_to_polygons_featurecollection("../City/Gandhinagar.geojson", "../City/Gandhinagar.geojson")
