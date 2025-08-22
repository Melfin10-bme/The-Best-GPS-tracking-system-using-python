# main.py
# This script simulates GPS tracking and visualizes the path on an interactive map.

# First, you need to install the required libraries.
# Open your terminal or command prompt and run:
# pip install folium geopy

import folium
from geopy.geocoders import Nominatim
import random
import time
import webbrowser
import os

def generate_random_path(start_lat, start_lon, num_points=50, max_step=0.001):
    """
    Generates a series of random GPS coordinates to simulate a path.

    Args:
        start_lat (float): The starting latitude.
        start_lon (float): The starting longitude.
        num_points (int): The number of points to generate for the path.
        max_step (float): The maximum random change for each coordinate step.

    Returns:
        list: A list of tuples, where each tuple is a (latitude, longitude) pair.
    """
    path = [(start_lat, start_lon)]
    current_lat, current_lon = start_lat, start_lon

    for _ in range(num_points - 1):
        # Generate a small random change to the current coordinates
        step_lat = random.uniform(-max_step, max_step)
        step_lon = random.uniform(-max_step, max_step)
        
        # Apply the change to create the next point in the path
        current_lat += step_lat
        current_lon += step_lon
        path.append((current_lat, current_lon))
        
    return path

def create_tracking_map(start_address):
    """
    Creates an interactive map with a simulated GPS track.

    Args:
        start_address (str): The starting address or location (e.g., "Eiffel Tower, Paris").
    """
    print(f"Finding coordinates for: {start_address}...")
    
    try:
        # Use geopy to get the coordinates for the starting address
        geolocator = Nominatim(user_agent="gps_tracker_app")
        location = geolocator.geocode(start_address)

        if not location:
            print(f"Error: Could not find coordinates for '{start_address}'. Please try a different location.")
            return

        start_lat, start_lon = location.latitude, location.longitude
        print(f"Coordinates found: ({start_lat}, {start_lon})")

        # Create a map centered at the starting location
        # You can change the zoom_start level to be more or less zoomed in.
        m = folium.Map(location=[start_lat, start_lon], zoom_start=15)

        # Generate the simulated GPS path
        print("Generating simulated GPS path...")
        gps_path = generate_random_path(start_lat, start_lon, num_points=100, max_step=0.0008)

        # Add the path to the map as a line
        folium.PolyLine(
            locations=gps_path,
            color='blue',
            weight=5,
            opacity=0.8
        ).add_to(m)

        # Add a marker for the start point
        folium.Marker(
            location=gps_path[0],
            popup='Start Point',
            icon=folium.Icon(color='green', icon='play')
        ).add_to(m)

        # Add a marker for the end point
        folium.Marker(
            location=gps_path[-1],
            popup='End Point',
            icon=folium.Icon(color='red', icon='stop')
        ).add_to(m)

        # Save the map to an HTML file
        map_file = 'gps_tracking_map.html'
        m.save(map_file)
        print(f"\nMap has been created successfully!")
        print(f"Saved as: {map_file}")

        # Automatically open the map in the default web browser
        webbrowser.open('file://' + os.path.realpath(map_file))

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your internet connection and make sure the location is valid.")

# --- Main part of the script ---
if __name__ == "__main__":
    # Ask the user to input a starting location.
    starting_location = input("Please enter a starting location (e.g., 'Eiffel Tower, Paris'): ")
    
    # Check if the user entered a location before proceeding.
    if starting_location.strip():
        create_tracking_map(starting_location)
    else:
        print("No location entered. Exiting program.")
