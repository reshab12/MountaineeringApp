import requests
import csv
import folium

# Overpass API endpoint
url = "https://overpass-api.de/api/interpreter"

# Overpass query for Bavaria (relation 51477), nodes/ways/relations, including center coordinates
query = """
[out:json][timeout:90];
relation(51477);              // Bavaria
map_to_area->.searchArea;
(
  node["natural"="peak"]["ele"](46.5,9.0,48.5,12.5);
  way["natural"="peak"]["ele"](46.5,9.0,48.5,12.5);
  relation["natural"="peak"]["ele"](46.5,9.0,48.5,12.5);
);
out center;
"""

print("Querying Overpass API...")
response = requests.get(url, params={'data': query})
response.raise_for_status()
data = response.json()
print(f"Total elements returned: {len(data['elements'])}")

# Process peaks
peaks = []
for element in data["elements"]:
    tags = element.get("tags", {})
    name = tags.get("name", "Unknown")
    ele_str = tags.get("ele", None)
    if ele_str:
        try:
            ele = float(ele_str.replace("m", "").replace(",", ".").strip())
            if ele > 2000:
                # Get coordinates
                if element["type"] == "node":
                    lat = element["lat"]
                    lon = element["lon"]
                else:  # way or relation
                    center = element.get("center")
                    if not center:
                        continue
                    lat = center["lat"]
                    lon = center["lon"]
                peaks.append((name, int(ele), lat, lon))
        except (ValueError, KeyError):
            continue

print(f"Peaks >2000m found: {len(peaks)}")

# Save CSV
csv_file = "bavarian_summits_over_2000mfull.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Elevation (m)", "lat", "lon"])
    writer.writerows(peaks)
print(f"Saved CSV: {csv_file}")

# Create Folium map
map_center = [48.5, 11.0]  # roughly central Bavaria
m = folium.Map(location=map_center, zoom_start=7)

for name, ele, lat, lon in peaks:
    folium.Marker(
        location=[lat, lon],
        popup=f"{name} ({ele} m)"
    ).add_to(m)

map_file = "bavarian_summits_map.html"
m.save(map_file)
print(f"Interactive map saved: {map_file}")
