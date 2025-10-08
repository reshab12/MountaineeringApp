import requests
import csv

# Try alternative servers if one fails
url = "https://overpass.kumi.systems/api/interpreter"
#url = "https://overpass-api.de/api/interpreter"

query = """
[out:json][timeout:90];
relation(51477);               // Germany's relation
map_to_area->.searchArea;      // convert relation to area
(
  node["natural"="peak"]["ele"](area.searchArea);
  way["natural"="peak"]["ele"](area.searchArea);
  relation["natural"="peak"]["ele"](area.searchArea);
);
out center;
"""

print("Querying Overpass API...")
response = requests.get(url, params={'data': query})
response.raise_for_status()
data = response.json()

print(f"Total peaks returned: {len(data['elements'])}")

peaks = []
for element in data["elements"]:
    tags = element.get("tags", {})
    name = tags.get("name", "Unknown")
    ele_str = tags.get("ele", None)
    if ele_str:
        try:
            ele = float(ele_str.replace("m", "").replace(",", ".").strip())
            if ele > 2000:
                peaks.append((name, int(ele), element['lat'], element['lon']))
        except ValueError:
            continue

with open("german_summits_over_2000m_new.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Elevation (m)", "lat", "lon"])
    writer.writerows(peaks)

print(f"Saved {len(peaks)} summits to german_summits_over_2000m_new.csv")
