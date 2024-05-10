from flask import Flask, render_template, request, send_file
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import io
import os

app = Flask(__name__)

""" @app.route('/')
def index():
    return render_template('form.html') """
    
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
    gpx_tree = ET.ElementTree(gpx)

    # Save to a memory buffer
    gpx_buffer = io.BytesIO()
    gpx_tree.write(gpx_buffer, encoding='utf-8', xml_declaration=True)
    gpx_buffer.seek(0)

    # Send the GPX file to the user
    return send_file(gpx_buffer, as_attachment=True, download_name="waypoints.gpx", mimetype="application/gpx+xml")

if __name__ == '__main__':
    app.run(debug=True)