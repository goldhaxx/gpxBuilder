from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

# Sample input data: list of (latitude, longitude) pairs
coordinates = [
    (32.80273799899065, -117.02562880661091),
    (32.804268, -117.026371)
]

# Initialize the root XML structure
gpx = ET.Element("gpx", version="1.1", creator="gpxBuilder Python Script")

# Starting timestamp
start_time = datetime(2024, 5, 7, 12, 0, 0)

# Create waypoint elements
for index, (lat, lon) in enumerate(coordinates):
    waypoint = ET.SubElement(gpx, "wpt", lat=str(lat), lon=str(lon))
    name = ET.SubElement(waypoint, "name")
    name.text = f"Waypoint {index + 1}"

    # Increment the timestamp for each waypoint
    time = ET.SubElement(waypoint, "time")
    waypoint_time = start_time + timedelta(minutes=index)
    time.text = waypoint_time.strftime("%Y-%m-%dT%H:%M:%SZ")

# Generate the XML tree structure
tree = ET.ElementTree(gpx)

# Write the XML to a GPX file
output_file = "waypoints.gpx"
tree.write(output_file, encoding="utf-8", xml_declaration=True)

print(f"GPX file with waypoints successfully created at {output_file}")