"""
PhysiCode - Geometry and Mesh Generation
Created by Jaime Estela | https://github.com/Jaimeestela | studio@jaimeestela.com

This module provides mesh generation algorithms and industrial analysis tools.
"""

from geometry.marching_cubes import generate_mesh
from geometry.industrial import analyze_geometry, calculate_volume, calculate_bounding_box

__all__ = ['generate_mesh', 'analyze_geometry', 'calculate_volume', 'calculate_bounding_box']
