from flask import Flask, render_template, request, send_file
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import io
import os
from geopy.distance import geodesic

app = Flask(__name__)

@app.route('/')
def index():
    # Retrieve the API key from the environment
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    return render_template('form.html', google_maps_api_key=google_maps_api_key)    

@app.route('/generate', methods=['POST'])
def generate_gpx():
    # Retrieve latitude and longitude data
    latitudes = request.form.getlist('lat[]')
    longitudes = request.form.getlist('lon[]')

    # Combine latitude and longitude pairs into a list of tuples
    coordinates = []
    for lat, lon in zip(latitudes, longitudes):
        if lat and lon:
            try:
                coordinates.append((float(lat), float(lon)))
            except ValueError:
                continue  # Ignore improperly formatted input

    # Initialize GPX root element
    gpx = ET.Element("gpx", version="1.1", creator="Flask Web App")

    # Starting timestamp
    start_time = datetime.now()

    # Create waypoint elements and calculate times based on distance
    current_time = start_time
    for index, coord in enumerate(coordinates):
        if index > 0:
            # Calculate distance between the current and previous waypoint
            distance = geodesic(coordinates[index - 1], coord).kilometers
            travel_time = timedelta(hours=distance / 10)  # Speed: 10 km/h
            current_time += travel_time
        
        waypoint = ET.SubElement(gpx, "wpt", lat=str(coord[0]), lon=str(coord[1]))
        ET.SubElement(waypoint, "name").text = f"Waypoint {index + 1}"
        ET.SubElement(waypoint, "time").text = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Generate the XML tree structure
    gpx_tree = ET.ElementTree(gpx)

    # Save to a memory buffer
    gpx_buffer = io.BytesIO()
    gpx_tree.write(gpx_buffer, encoding='utf-8', xml_declaration=True)
    gpx_buffer.seek(0)

    # Send the GPX file to the user
    return send_file(gpx_buffer, as_attachment=True, download_name="waypoints.gpx", mimetype="application/gpx+xml")

if __name__ == '__main__':
    app.run(debug=True)
