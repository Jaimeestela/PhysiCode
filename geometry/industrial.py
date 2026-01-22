"""
Industrial Analysis Tools
Created by Jaime Estela | https://github.com/Jaimeestela | studio@jaimeestela.com

This module provides industrial analysis tools for generated geometries,
including volume calculation, bounding box analysis, and manufacturing
validation.
"""

import numpy as np
import trimesh
from typing import Dict, Tuple, Optional


def calculate_volume(mesh: trimesh.Trimesh) -> float:
    """
    Calculate the volume of a closed mesh.
    
    The volume is calculated using the divergence theorem (Gauss's theorem),
    which integrates over the mesh surface. For open meshes, the volume
    may not be meaningful.
    
    Parameters
    ----------
    mesh : trimesh.Trimesh
        The mesh to calculate volume for
    
    Returns
    -------
    float
        Volume in cubic units (same units as mesh vertices)
    
    Examples
    --------
    >>> mesh = trimesh.creation.box()
    >>> volume = calculate_volume(mesh)
    >>> print(f"Volume: {volume:.2f} mm³")
    """
    if not mesh.is_volume:
        # For open meshes, return 0 or surface area
        return 0.0
    
    return float(mesh.volume)


def calculate_bounding_box(mesh: trimesh.Trimesh) -> Dict[str, Tuple[float, float]]:
    """
    Calculate the axis-aligned bounding box of a mesh.
    
    Returns the minimum and maximum coordinates along each axis,
    which is useful for manufacturing constraints and material estimation.
    
    Parameters
    ----------
    mesh : trimesh.Trimesh
        The mesh to analyze
    
    Returns
    -------
    dict
        Dictionary with keys 'x', 'y', 'z', each containing a tuple
        of (min, max) coordinates
    
    Examples
    --------
    >>> mesh = trimesh.creation.box()
    >>> bbox = calculate_bounding_box(mesh)
    >>> print(f"X range: {bbox['x']}")
    """
    bounds = mesh.bounds
    
    return {
        'x': (float(bounds[0, 0]), float(bounds[1, 0])),
        'y': (float(bounds[0, 1]), float(bounds[1, 1])),
        'z': (float(bounds[0, 2]), float(bounds[1, 2]))
    }


def calculate_dimensions(mesh: trimesh.Trimesh) -> Dict[str, float]:
    """
    Calculate the dimensions (width, height, depth) of a mesh.
    
    Parameters
    ----------
    mesh : trimesh.Trimesh
        The mesh to analyze
    
    Returns
    -------
    dict
        Dictionary with keys 'width', 'height', 'depth' containing
        the size along each axis
    
    Examples
    --------
    >>> mesh = trimesh.creation.box()
    >>> dims = calculate_dimensions(mesh)
    >>> print(f"Dimensions: {dims}")
    """
    bbox = calculate_bounding_box(mesh)
    
    return {
        'width': bbox['x'][1] - bbox['x'][0],
        'height': bbox['y'][1] - bbox['y'][0],
        'depth': bbox['z'][1] - bbox['z'][0]
    }


def analyze_geometry(mesh: trimesh.Trimesh) -> Dict:
    """
    Perform comprehensive industrial analysis of a mesh.
    
    This function calculates volume, bounding box, dimensions, surface area,
    and other metrics useful for manufacturing and material estimation.
    
    Parameters
    ----------
    mesh : trimesh.Trimesh
        The mesh to analyze
    
    Returns
    -------
    dict
        Dictionary containing:
        - 'volume': float - Volume in cubic units
        - 'surface_area': float - Surface area in square units
        - 'bbox': dict - Bounding box coordinates
        - 'dimensions': dict - Width, height, depth
        - 'is_watertight': bool - Whether mesh is closed
        - 'vertex_count': int - Number of vertices
        - 'face_count': int - Number of faces
    
    Examples
    --------
    >>> mesh = generate_mesh(gyroid, resolution=50)
    >>> analysis = analyze_geometry(mesh)
    >>> print(f"Volume: {analysis['volume']:.2f} mm³")
    >>> print(f"Dimensions: {analysis['dimensions']}")
    """
    bbox = calculate_bounding_box(mesh)
    dimensions = calculate_dimensions(mesh)
    volume = calculate_volume(mesh)
    
    return {
        'volume': volume,
        'surface_area': float(mesh.area),
        'bbox': bbox,
        'dimensions': dimensions,
        'is_watertight': mesh.is_watertight,
        'is_volume': mesh.is_volume,
        'vertex_count': len(mesh.vertices),
        'face_count': len(mesh.faces),
        'edge_count': len(mesh.edges)
    }


def estimate_material_usage(mesh: trimesh.Trimesh, 
                            material_density: float = 1.0,
                            wall_thickness: Optional[float] = None) -> Dict[str, float]:
    """
    Estimate material usage for manufacturing.
    
    For solid parts, calculates mass based on volume and density.
    For shell parts, calculates material based on surface area and wall thickness.
    
    Parameters
    ----------
    mesh : trimesh.Trimesh
        The mesh to analyze
    material_density : float, optional
        Material density in g/cm³, by default 1.0
    wall_thickness : float, optional
        Wall thickness for shell parts in mm, by default None (solid part)
    
    Returns
    -------
    dict
        Dictionary containing:
        - 'volume': float - Volume in mm³
        - 'mass': float - Estimated mass in grams
        - 'material_volume': float - Actual material volume (accounting for shells)
    
    Examples
    --------
    >>> mesh = generate_mesh(gyroid, resolution=50)
    >>> # For PLA plastic (density ~1.24 g/cm³)
    >>> usage = estimate_material_usage(mesh, material_density=1.24)
    >>> print(f"Estimated mass: {usage['mass']:.2f} g")
    """
    volume_mm3 = calculate_volume(mesh)
    
    if wall_thickness is not None and wall_thickness > 0:
        # Shell part: material volume = surface area * thickness
        surface_area_mm2 = mesh.area
        material_volume_mm3 = surface_area_mm2 * wall_thickness
    else:
        # Solid part
        material_volume_mm3 = volume_mm3
    
    # Convert mm³ to cm³ and calculate mass
    volume_cm3 = material_volume_mm3 / 1000.0
    mass_g = volume_cm3 * material_density
    
    return {
        'volume': volume_mm3,
        'material_volume': material_volume_mm3,
        'mass': mass_g,
        'density': material_density
    }
