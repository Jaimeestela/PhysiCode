"""
Batch Export Example
Created by Jaime Estela | https://github.com/Jaimeestela | studio@jaimeestela.com

This example demonstrates how to generate multiple geometries with varying
parameters and export them in batch for parametric design workflows.
"""

import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tpms import Gyroid, SchwarzP
from geometry.marching_cubes import generate_mesh
from geometry.industrial import analyze_geometry, estimate_material_usage


def batch_gyroid_variations():
    """Generate multiple Gyroid variations with different scales."""
    print("Generating Gyroid variations...")
    
    scales = [8.0, 10.0, 12.0, 15.0]
    results = []
    
    for scale in scales:
        print(f"\n  Processing scale={scale}...")
        
        gyroid = Gyroid(scale=scale, thickness=0.0)
        mesh = generate_mesh(
            gyroid,
            resolution=40,
            iso_value=0.0,
            bounds=((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0))
        )
        
        analysis = analyze_geometry(mesh)
        material = estimate_material_usage(mesh, material_density=1.24)  # PLA density
        
        results.append({
            'scale': scale,
            'volume': analysis['volume'],
            'mass': material['mass'],
            'mesh': mesh
        })
        
        # Export
        filename = f"gyroid_scale_{scale:.1f}.stl"
        mesh.export(filename)
        print(f"    ✅ Exported: {filename}")
        print(f"    Volume: {analysis['volume']:.2f} mm³")
        print(f"    Estimated mass: {material['mass']:.2f} g")
    
    return results


def batch_thickness_variations():
    """Generate Gyroid variations with different thickness values."""
    print("\nGenerating thickness variations...")
    
    thicknesses = [0.0, 0.3, 0.5, 0.7, 1.0]
    results = []
    
    for thickness in thicknesses:
        print(f"\n  Processing thickness={thickness}...")
        
        gyroid = Gyroid(scale=10.0, thickness=thickness)
        mesh = generate_mesh(
            gyroid,
            resolution=40,
            iso_value=0.0,
            bounds=((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0))
        )
        
        analysis = analyze_geometry(mesh)
        
        results.append({
            'thickness': thickness,
            'volume': analysis['volume'],
            'surface_area': analysis['surface_area'],
            'mesh': mesh
        })
        
        # Export
        filename = f"gyroid_thickness_{thickness:.1f}.stl"
        mesh.export(filename)
        print(f"    ✅ Exported: {filename}")
        print(f"    Volume: {analysis['volume']:.2f} mm³")
        print(f"    Surface Area: {analysis['surface_area']:.2f} mm²")
    
    return results


def parametric_study():
    """Perform a parametric study of resolution vs. mesh quality."""
    print("\nPerforming parametric study: Resolution vs. Quality...")
    
    resolutions = [20, 30, 40, 50, 60]
    results = []
    
    gyroid = Gyroid(scale=10.0, thickness=0.0)
    
    for resolution in resolutions:
        print(f"\n  Processing resolution={resolution}...")
        
        mesh = generate_mesh(
            gyroid,
            resolution=resolution,
            iso_value=0.0,
            bounds=((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0))
        )
        
        analysis = analyze_geometry(mesh)
        
        results.append({
            'resolution': resolution,
            'vertices': analysis['vertex_count'],
            'faces': analysis['face_count'],
            'volume': analysis['volume'],
            'mesh': mesh
        })
        
        print(f"    Vertices: {analysis['vertex_count']:,}")
        print(f"    Faces: {analysis['face_count']:,}")
        print(f"    Volume: {analysis['volume']:.2f} mm³")
    
    # Summary
    print("\n  Summary:")
    print("  Resolution | Vertices | Faces    | Volume")
    print("  " + "-" * 45)
    for r in results:
        print(f"  {r['resolution']:10d} | {r['vertices']:8,} | {r['faces']:7,} | {r['volume']:7.2f}")
    
    return results


if __name__ == "__main__":
    print("=" * 60)
    print("PhysiCode - Batch Export Example")
    print("=" * 60)
    print("\nThis example demonstrates parametric design workflows\n")
    
    # Run batch operations
    scale_results = batch_gyroid_variations()
    thickness_results = batch_thickness_variations()
    parametric_results = parametric_study()
    
    print("\n" + "=" * 60)
    print("✅ Batch export completed successfully!")
    print(f"   Generated {len(scale_results) + len(thickness_results)} STL files")
    print("=" * 60)
