import streamlit as st
import plotly.graph_objects as go
import numpy as np
import shape 

st.title("Shape Formation Visualizer")

# User inputs
shape_name = st.selectbox("Choose a shape", ["circle", "square", "triangle","cube", "sphere", "pyramid"])
formation_name = st.selectbox("Choose a formation", ["grid", "radial", "spiral", "cuboid", "sphere"])

shape_size = st.number_input("Shape size", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
spacing = st.number_input("Spacing", min_value=0.0, max_value=5.0, value=0.5, step=0.1)
count = st.number_input("Count (radial/spiral/sphere)", min_value=1, max_value=200, value=20, step=1)

f_size1 = st.number_input("Formation size 1", min_value=1, max_value=50, value=10, step=1)
f_size2 = st.number_input("Formation size 2", min_value=1, max_value=50, value=10, step=1)
f_size3 = st.number_input("Formation size 3", min_value=1, max_value=50, value=10, step=1)

r_step = st.number_input("Radius step size (spiral)", min_value=0.5, max_value=5.0, value=0.5, step=0.5)
theta_step = st.number_input("Angle step size (spiral)", min_value=1, max_value=360, value=10, step=1)
height_step = st.number_input("Height step size (spiral)", min_value=0, max_value=50, value=1, step=1)

# Create the scene for the given inputs
scene = shape.create_mesh(shape_name, formation_name, shape_size, spacing, f_size1, f_size2, f_size3, count, r_step, theta_step, height_step)

# Make a Plotly 3D figure
fig = go.Figure()

for geom in scene.geometry.values():   # iterate all Trimesh meshes in the Scene
    x, y, z = geom.vertices.T
    i, j, k = geom.faces.T

    fig.add_trace(go.Mesh3d(
        x=x, y=y, z=z,
        i=i, j=j, k=k,
        color='lightblue',
        opacity=0.5
    ))

fig.update_layout(scene=dict(aspectmode="data"))
st.plotly_chart(fig, use_container_width=True)