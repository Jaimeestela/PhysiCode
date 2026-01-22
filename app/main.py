"""
PhysiCode - Interactive Playground
Created by Jaime Estela | https://github.com/Jaimeestela | studio@jaimeestela.com

Streamlit application for interactive generation and visualization of
mathematical geometries.
"""

import streamlit as st
import numpy as np
import trimesh
import plotly.graph_objects as go
from io import BytesIO

from core.tpms import Gyroid, SchwarzP
from geometry.marching_cubes import generate_mesh
from geometry.industrial import analyze_geometry

# Page configuration
st.set_page_config(
    page_title="PhysiCode - Engineering as Code",
    page_icon="🔬",
    layout="wide"
)

# Header
st.title("🔬 PhysiCode: Engineering-as-Code Playground")
st.markdown("""
**Transform mathematical functions into manufacturable 3D geometry**

*Created by [Jaime Estela](https://github.com/Jaimeestela) | [Contact](mailto:studio@jaimeestela.com)*
""")

# Sidebar for controls
st.sidebar.header("🎛️ Controls")

# Primitive selection
primitive_type = st.sidebar.selectbox(
    "Mathematical Primitive",
    ["Gyroid TPMS", "Schwarz P TPMS"],
    help="Select the mathematical surface to generate"
)

# Parameters
st.sidebar.subheader("Parameters")

scale = st.sidebar.slider(
    "Scale",
    min_value=1.0,
    max_value=20.0,
    value=10.0,
    step=0.5,
    help="Scaling factor for the periodic structure"
)

thickness = st.sidebar.slider(
    "Thickness",
    min_value=0.0,
    max_value=2.0,
    value=0.0,
    step=0.1,
    help="Wall thickness for solid volumes (0 = surface only)"
)

resolution = st.sidebar.slider(
    "Resolution",
    min_value=20,
    max_value=100,
    value=50,
    step=5,
    help="Number of sample points along each axis (higher = smoother but slower)"
)

iso_value = st.sidebar.slider(
    "Iso-value",
    min_value=-2.0,
    max_value=2.0,
    value=0.0,
    step=0.1,
    help="Iso-surface extraction level"
)

# Bounds
st.sidebar.subheader("Bounds")
bounds_x = st.sidebar.slider(
    "X Range",
    min_value=-10.0,
    max_value=10.0,
    value=(-5.0, 5.0),
    help="X-axis bounds"
)
bounds_y = st.sidebar.slider(
    "Y Range",
    min_value=-10.0,
    max_value=10.0,
    value=(-5.0, 5.0),
    help="Y-axis bounds"
)
bounds_z = st.sidebar.slider(
    "Z Range",
    min_value=-10.0,
    max_value=10.0,
    value=(-5.0, 5.0),
    help="Z-axis bounds"
)

bounds = (bounds_x, bounds_y, bounds_z)

# Generate button
generate_button = st.sidebar.button("🚀 Generate Geometry", type="primary")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("3D Visualization")
    
    if generate_button or 'mesh' not in st.session_state:
        with st.spinner("Generating geometry..."):
            # Create field based on selection
            if primitive_type == "Gyroid TPMS":
                field = Gyroid(scale=scale, thickness=thickness)
            else:  # Schwarz P TPMS
                field = SchwarzP(scale=scale, thickness=thickness)
            
            # Generate mesh
            try:
                mesh = generate_mesh(
                    field,
                    resolution=resolution,
                    iso_value=iso_value,
                    bounds=bounds
                )
                
                if len(mesh.vertices) > 0:
                    st.session_state['mesh'] = mesh
                    st.session_state['field'] = primitive_type
                    st.success("✅ Geometry generated successfully!")
                else:
                    st.error("❌ Generated mesh is empty. Try adjusting parameters.")
                    st.session_state['mesh'] = None
            except Exception as e:
                st.error(f"❌ Error generating geometry: {str(e)}")
                st.session_state['mesh'] = None
    
    # Visualize mesh
    if 'mesh' in st.session_state and st.session_state['mesh'] is not None:
        mesh = st.session_state['mesh']
        
        # Create 3D plot
        fig = go.Figure(data=[
            go.Mesh3d(
                x=mesh.vertices[:, 0],
                y=mesh.vertices[:, 1],
                z=mesh.vertices[:, 2],
                i=mesh.faces[:, 0],
                j=mesh.faces[:, 1],
                k=mesh.faces[:, 2],
                colorscale='Viridis',
                intensity=mesh.vertices[:, 2],
                showscale=True,
                name='Geometry'
            )
        ])
        
        fig.update_layout(
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Z",
                aspectmode='data'
            ),
            height=600,
            title="Interactive 3D Geometry"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👆 Click 'Generate Geometry' to create your first shape!")

with col2:
    st.subheader("📊 Analysis")
    
    if 'mesh' in st.session_state and st.session_state['mesh'] is not None:
        mesh = st.session_state['mesh']
        analysis = analyze_geometry(mesh)
        
        st.metric("Volume", f"{analysis['volume']:.2f} mm³")
        st.metric("Surface Area", f"{analysis['surface_area']:.2f} mm²")
        
        st.markdown("### Dimensions")
        dims = analysis['dimensions']
        st.write(f"**Width:** {dims['width']:.2f} mm")
        st.write(f"**Height:** {dims['height']:.2f} mm")
        st.write(f"**Depth:** {dims['depth']:.2f} mm")
        
        st.markdown("### Mesh Info")
        st.write(f"**Vertices:** {analysis['vertex_count']:,}")
        st.write(f"**Faces:** {analysis['face_count']:,}")
        st.write(f"**Edges:** {analysis['edge_count']:,}")
        
        st.write(f"**Watertight:** {'✅' if analysis['is_watertight'] else '❌'}")
        st.write(f"**Volume:** {'✅' if analysis['is_volume'] else '❌'}")
        
        # Download button
        st.markdown("---")
        st.subheader("💾 Export")
        
        if st.button("Download STL"):
            if mesh is not None:
                # Export to bytes
                buffer = BytesIO()
                mesh.export(buffer, file_type='stl')
                buffer.seek(0)
                
                st.download_button(
                    label="⬇️ Download STL File",
                    data=buffer,
                    file_name=f"{primitive_type.lower().replace(' ', '_')}_{scale}_{resolution}.stl",
                    mime="application/octet-stream"
                )
    else:
        st.info("Generate a geometry to see analysis results.")

# Footer
st.markdown("---")
st.markdown("""
<div align="center">
<small>
<strong>PhysiCode</strong> - Engineering-as-Code Toolkit<br>
Created by <a href="https://github.com/Jaimeestela">Jaime Estela</a> | 
<a href="mailto:studio@jaimeestela.com">Contact</a> | 
<a href="https://github.com/Jaimeestela/PhysiCode">GitHub</a><br>
Licensed under Apache License 2.0
</small>
</div>
""", unsafe_allow_html=True)
