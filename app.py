import streamlit as st
import requests
import pyvista as pv
from stpyvista import stpyvista
import numpy as np
import rasterio

def download_dem(north, south, east, west, output_file):
    # OpenTopography API endpoint
    url = "https://portal.opentopography.org/API/globaldem"
    
    # Parameters for the API request
    params = {
        "demtype": "SRTMGL1",  # SRTM GL1 (30m)
        "south": south,
        "north": north,
        "west": west,
        "east": east,
        "outputFormat": "GTiff",
        "API_Key": "d216151dff28d69ee4eebe7d5bd65de7"  # Replace with your API key if you have one
    }
    
    st.write("Downloading DEM...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        st.write(f"DEM downloaded and saved as {output_file}")
    else:
        st.write(f"Error downloading DEM. Status code: {response.status_code}")
        st.write(f"Response: {response.text}")

def visualize_dem(dem_file):
    # Read DEM file
    with rasterio.open(dem_file) as src:
        elevation = src.read(1)
        transform = src.transform

    # Generate X, Y coordinates
    x = np.arange(elevation.shape[1])
    y = np.arange(elevation.shape[0])
    x, y = np.meshgrid(x, y)

    # Transform coordinates
    x, y = np.array(transform * (x, y))

    # Create a PyVista mesh
    mesh = pv.StructuredGrid(x, y, elevation)

    # Add a scalar field (elevation) associated with the mesh
    mesh['elevation'] = elevation.flatten()

    # Initialize a plotter object
    plotter = pv.Plotter(window_size=[800, 800])

    # Add mesh to the plotter
    plotter.add_mesh(mesh, scalars='elevation', cmap='terrain')

    # Final touches
    plotter.view_isometric()
    plotter.background_color = 'white'

    # Send to Streamlit using stpyvista
    stpyvista(plotter, key="pv_dem")

# Streamlit UI
st.title("DEM Visualization with PyVista and Streamlit")

# Define area of interest
north = st.number_input("North Latitude", value=39.44362)
south = st.number_input("South Latitude", value=39.375)
east = st.number_input("East Longitude", value=-76.23542)
west = st.number_input("West Longitude", value=-76.363)

output_file = "alps_dem.tif"

if st.button("Download and Visualize DEM"):
    download_dem(north, south, east, west, output_file)
    visualize_dem(output_file)
