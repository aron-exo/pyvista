import streamlit as st
import pyvista as pv
import numpy as np
from stpyvista import stpyvista

"# 🧱 Structured grid"

## Create coordinate data
x = np.arange(-10, 10, 0.25)
y = np.arange(-10, 10, 0.25)
x, y = np.meshgrid(x, y)
z = np.sin(np.sqrt(x**2 + y**2))

## Set up plotter
plotter = pv.Plotter(window_size=[600,600])
surface = pv.StructuredGrid(x, y, z)
plotter.add_mesh(surface, color='teal', show_edges=True)

## Pass the plotter (not the mesh) to stpyvista
stpyvista(plotter, key="surface")
