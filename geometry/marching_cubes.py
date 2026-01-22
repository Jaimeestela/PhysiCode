"""
Marching Cubes Algorithm for Mesh Generation
Created by Jaime Estela | https://github.com/Jaimeestela | studio@jaimeestela.com

This module implements the Marching Cubes algorithm to extract triangular
meshes from scalar fields. The algorithm generates iso-surfaces by sampling
the field on a regular grid and creating triangles based on the field values
at grid vertices.
"""

import numpy as np
import trimesh
from typing import Tuple, Optional
from scipy.spatial import Delaunay
from scipy.ndimage import map_coordinates

from core.fields import ScalarField


def generate_mesh(field: ScalarField, 
                  resolution: int = 50,
                  iso_value: float = 0.0,
                  bounds: Optional[Tuple[Tuple[float, float], 
                                        Tuple[float, float], 
                                        Tuple[float, float]]] = None) -> trimesh.Trimesh:
    """
    Generate a triangular mesh from a scalar field using the Marching Cubes algorithm.
    
    This function samples the scalar field on a regular 3D grid and extracts
    an iso-surface at the specified iso-value using the Marching Cubes algorithm.
    
    Parameters
    ----------
    field : ScalarField
        The scalar field to extract the mesh from
    resolution : int, optional
        Number of sample points along each axis, by default 50
    iso_value : float, optional
        Iso-value at which to extract the surface, by default 0.0
    bounds : tuple of tuples, optional
        Bounding box as ((x_min, x_max), (y_min, y_max), (z_min, z_max)),
        by default None (uses (-5, 5) for each axis)
    
    Returns
    -------
    trimesh.Trimesh
        Triangular mesh representing the iso-surface
    
    Examples
    --------
    >>> from core.tpms import Gyroid
    >>> gyroid = Gyroid(scale=10.0)
    >>> mesh = generate_mesh(gyroid, resolution=50, iso_value=0.0)
    >>> mesh.export('gyroid.stl')
    """
    # Set default bounds if not provided
    if bounds is None:
        bounds = ((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0))
    
    x_min, x_max = bounds[0]
    y_min, y_max = bounds[1]
    z_min, z_max = bounds[2]
    
    # Create coordinate grids
    x = np.linspace(x_min, x_max, resolution)
    y = np.linspace(y_min, y_max, resolution)
    z = np.linspace(z_min, z_max, resolution)
    
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    
    # Evaluate field on grid
    field_values = field(X, Y, Z)
    
    # Use scipy's marching cubes implementation (more robust)
    try:
        from skimage import measure
        # scikit-image has a well-tested marching cubes implementation
        vertices, faces, normals, values = measure.marching_cubes(
            field_values, 
            level=iso_value,
            spacing=(
                (x_max - x_min) / (resolution - 1),
                (y_max - y_min) / (resolution - 1),
                (z_max - z_min) / (resolution - 1)
            ),
            origin=(x_min, y_min, z_min)
        )
        
        # Create trimesh object
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces, vertex_normals=normals)
        
    except ImportError:
        # Fallback: use trimesh's marching cubes if scikit-image not available
        # This is a simplified implementation
        mesh = _marching_cubes_simple(field, resolution, iso_value, bounds)
    
    # Clean up mesh
    mesh.remove_duplicate_faces()
    mesh.remove_unreferenced_vertices()
    
    return mesh


def _marching_cubes_simple(field: ScalarField,
                           resolution: int,
                           iso_value: float,
                           bounds: Tuple[Tuple[float, float], 
                                        Tuple[float, float], 
                                        Tuple[float, float]]) -> trimesh.Trimesh:
    """
    Simplified marching cubes implementation using trimesh.
    
    This is a fallback when scikit-image is not available.
    """
    x_min, x_max = bounds[0]
    y_min, y_max = bounds[1]
    z_min, z_max = bounds[2]
    
    # Create a dense point cloud by sampling the field
    x = np.linspace(x_min, x_max, resolution)
    y = np.linspace(y_min, y_max, resolution)
    z = np.linspace(z_min, z_max, resolution)
    
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    field_values = field(X, Y, Z)
    
    # Find points near the iso-surface
    mask = np.abs(field_values - iso_value) < 0.1 * np.std(field_values)
    points = np.stack([X[mask], Y[mask], Z[mask]], axis=1)
    
    if len(points) < 4:
        # Not enough points, return empty mesh
        return trimesh.Trimesh()
    
    # Create mesh from point cloud using Delaunay triangulation
    # This is a simplified approach - full marching cubes would be more accurate
    try:
        tri = Delaunay(points)
        mesh = trimesh.Trimesh(vertices=points, faces=tri.simplices)
        
        # Remove degenerate faces
        mesh = mesh[mesh.area > 1e-10]
        
        return mesh
    except:
        # If triangulation fails, return empty mesh
        return trimesh.Trimesh()
