"""
Basic TPMS Generation Example
Created by Jaime Estela | https://github.com/Jaimeestela | studio@jaimeestela.com

This example demonstrates how to generate basic TPMS surfaces (Gyroid and Schwarz P)
and export them as STL files for 3D printing.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tpms import Gyroid, SchwarzP
from geometry.marching_cubes import generate_mesh
from geometry.industrial import analyze_geometry


def generate_gyroid_example():
    """Generate a Gyroid TPMS surface."""
    print("Generating Gyroid TPMS surface...")
    
    # Create Gyroid field
    gyroid = Gyroid(scale=10.0, thickness=0.0)
    
    # Generate mesh
    mesh = generate_mesh(
        gyroid,
        resolution=50,
        iso_value=0.0,
        bounds=((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0))
    )
    
    # Analyze geometry
    analysis = analyze_geometry(mesh)
    print(f"\nGyroid Analysis:")
    print(f"  Volume: {analysis['volume']:.2f} mm³")
    print(f"  Surface Area: {analysis['surface_area']:.2f} mm²")
    print(f"  Dimensions: {analysis['dimensions']}")
    print(f"  Vertices: {analysis['vertex_count']:,}")
    print(f"  Faces: {analysis['face_count']:,}")
    
    # Export STL
    output_file = "gyroid_surface.stl"
    mesh.export(output_file)
    print(f"\n[OK] Exported to: {output_file}")
    
    return mesh


def generate_schwarz_p_example():
    """Generate a Schwarz P TPMS surface."""
    print("\nGenerating Schwarz P TPMS surface...")
    
    # Create Schwarz P field
    schwarz_p = SchwarzP(scale=8.0, thickness=0.0)
    
    # Generate mesh
    mesh = generate_mesh(
        schwarz_p,
        resolution=50,
        iso_value=0.0,
        bounds=((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0))
    )
    
    # Analyze geometry
    analysis = analyze_geometry(mesh)
    print(f"\nSchwarz P Analysis:")
    print(f"  Volume: {analysis['volume']:.2f} mm³")
    print(f"  Surface Area: {analysis['surface_area']:.2f} mm²")
    print(f"  Dimensions: {analysis['dimensions']}")
    print(f"  Vertices: {analysis['vertex_count']:,}")
    print(f"  Faces: {analysis['face_count']:,}")
    
    # Export STL
    output_file = "schwarz_p_surface.stl"
    mesh.export(output_file)
    print(f"\n[OK] Exported to: {output_file}")
    
    return mesh


def generate_solid_gyroid_example():
    """Generate a solid Gyroid with wall thickness."""
    print("\nGenerating solid Gyroid with thickness...")
    
    # Create solid Gyroid (with thickness)
    gyroid = Gyroid(scale=10.0, thickness=0.5)
    
    # Generate mesh
    mesh = generate_mesh(
        gyroid,
        resolution=50,
        iso_value=0.0,
        bounds=((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0))
    )
    
    # Analyze geometry
    analysis = analyze_geometry(mesh)
    print(f"\nSolid Gyroid Analysis:")
    print(f"  Volume: {analysis['volume']:.2f} mm³")
    print(f"  Surface Area: {analysis['surface_area']:.2f} mm²")
    print(f"  Is Watertight: {analysis['is_watertight']}")
    
    # Export STL
    output_file = "gyroid_solid.stl"
    mesh.export(output_file)
    print(f"\n[OK] Exported to: {output_file}")
    
    return mesh


if __name__ == "__main__":
    print("=" * 60)
    print("PhysiCode - Basic TPMS Generation Example")
    print("=" * 60)
    
    # Generate examples
    gyroid_mesh = generate_gyroid_example()
    schwarz_mesh = generate_schwarz_p_example()
    solid_mesh = generate_solid_gyroid_example()
    
    print("\n" + "=" * 60)
    print("[OK] All examples completed successfully!")
    print("=" * 60)
