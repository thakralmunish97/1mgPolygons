import folium
import json


geojson_path = '../Polygons/1MG_DSN_6000M_KOL_DEC_29_2025.geojson'

with open(geojson_path, 'r') as f:
    data = json.load(f)

m = folium.Map(location=[28.6139, 77.2090], zoom_start=12)  # Delhi example


def extract_boundary_points(geojson_data):
    points = []

    def recurse(geom):
        if geom['type'] == 'Polygon':
            for ring in geom['coordinates']:  # Exterior + interiors
                for coord in ring:
                    points.append([coord[1], coord[0]])  # [lat, lng]
        elif geom['type'] == 'MultiPolygon':
            for poly in geom['coordinates']:
                recurse({'type': 'Polygon', 'coordinates': poly})
        elif geom['type'] == 'LineString':
            for coord in geom['coordinates']:
                points.append([coord[1], coord[0]])
        elif geom['type'] == 'MultiLineString':
            for line in geom['coordinates']:
                for coord in line:
                    points.append([coord[1], coord[0]])

    for feature in geojson_data['features']:
        recurse(feature['geometry'])

    return list(set(tuple(p) for p in points))  # Dedupe


boundary_pts = extract_boundary_points(data)

# Add GeoJSON boundaries (transparent fill)
folium.GeoJson(
    data,
    style_function=lambda x: {'color': 'black', 'weight': 2, 'fillOpacity': 0}
).add_to(m)

# Markers ONLY on boundary points with coords popup
for pt in boundary_pts:
    folium.Marker(
        pt,
        popup=f"Boundary Point: [{pt[0]:.4f}, {pt[1]:.4f}]",
        icon=folium.Icon(color='red', icon='map-marker', icon_size=(12, 12))
    ).add_to(m)

m.save('boundary_points.html')
m
