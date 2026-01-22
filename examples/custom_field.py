"""
Custom Scalar Field Example
Created by Jaime Estela | https://github.com/Jaimeestela | studio@jaimeestela.com

This example demonstrates how to create custom scalar fields by subclassing
the ScalarField base class.
"""

import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.fields import ScalarField
from geometry.marching_cubes import generate_mesh
from geometry.industrial import analyze_geometry


class SinusoidalField(ScalarField):
    """
    A custom scalar field defined by sinusoidal functions.
    
    Mathematical definition:
        f(x, y, z) = sin(x) * cos(y) * sin(z)
    """
    
    def evaluate(self, x, y, z):
        """Evaluate the sinusoidal field."""
        return np.sin(x) * np.cos(y) * np.sin(z)


class SphericalField(ScalarField):
    """
    A spherical distance field.
    
    Creates a sphere at the origin with radius defined by scale.
    """
    
    def evaluate(self, x, y, z):
        """Evaluate the spherical field."""
        # Distance from origin
        r = np.sqrt(x**2 + y**2 + z**2)
        # Return signed distance (negative inside, positive outside)
        return r - self.scale


class TorusField(ScalarField):
    """
    A torus field.
    
    Creates a torus with major radius R and minor radius r.
    """
    
    def __init__(self, scale=1.0, major_radius=3.0, minor_radius=1.0):
        super().__init__(scale=scale)
        self.major_radius = major_radius
        self.minor_radius = minor_radius
    
    def evaluate(self, x, y, z):
        """Evaluate the torus field."""
        # Distance from torus center in XY plane
        xy_dist = np.sqrt(x**2 + y**2) - self.major_radius
        # Distance from torus surface
        return np.sqrt(xy_dist**2 + z**2) - self.minor_radius


def example_sinusoidal():
    """Generate geometry from sinusoidal field."""
    print("Generating geometry from Sinusoidal Field...")
    
    field = SinusoidalField(scale=2.0)
    mesh = generate_mesh(
        field,
        resolution=40,
        iso_value=0.0,
        bounds=((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0))
    )
    
    analysis = analyze_geometry(mesh)
    print(f"  Volume: {analysis['volume']:.2f} mm³")
    print(f"  Surface Area: {analysis['surface_area']:.2f} mm²")
    
    mesh.export("sinusoidal_field.stl")
    print("✅ Exported to: sinusoidal_field.stl\n")
    
    return mesh


def example_sphere():
    """Generate geometry from spherical field."""
    print("Generating geometry from Spherical Field...")
    
    field = SphericalField(scale=3.0)
    mesh = generate_mesh(
        field,
        resolution=50,
        iso_value=0.0,
        bounds=((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0))
    )
    
    analysis = analyze_geometry(mesh)
    print(f"  Volume: {analysis['volume']:.2f} mm³")
    print(f"  Surface Area: {analysis['surface_area']:.2f} mm²")
    print(f"  Expected radius: 3.0")
    
    mesh.export("sphere_field.stl")
    print("✅ Exported to: sphere_field.stl\n")
    
    return mesh


def example_torus():
    """Generate geometry from torus field."""
    print("Generating geometry from Torus Field...")
    
    field = TorusField(scale=1.0, major_radius=3.0, minor_radius=1.0)
    mesh = generate_mesh(
        field,
        resolution=50,
        iso_value=0.0,
        bounds=((-6.0, 6.0), (-6.0, 6.0), (-3.0, 3.0))
    )
    
    analysis = analyze_geometry(mesh)
    print(f"  Volume: {analysis['volume']:.2f} mm³")
    print(f"  Surface Area: {analysis['surface_area']:.2f} mm²")
    
    mesh.export("torus_field.stl")
    print("✅ Exported to: torus_field.stl\n")
    
    return mesh


if __name__ == "__main__":
    print("=" * 60)
    print("PhysiCode - Custom Scalar Field Example")
    print("=" * 60)
    print("\nThis example demonstrates creating custom scalar fields\n")
    
    # Run examples
    example_sinusoidal()
    example_sphere()
    example_torus()
    
    print("=" * 60)
    print("✅ All custom field examples completed!")
    print("=" * 60)
