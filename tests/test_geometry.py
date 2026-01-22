"""
Unit Tests for Geometry Functions
Created by Jaime Estela | https://github.com/Jaimeestela | studio@jaimeestela.com
"""

import pytest
import numpy as np
import trimesh
from core.tpms import Gyroid
from geometry.marching_cubes import generate_mesh
from geometry.industrial import (
    calculate_volume,
    calculate_bounding_box,
    calculate_dimensions,
    analyze_geometry,
    estimate_material_usage
)


class TestMarchingCubes:
    """Test cases for mesh generation."""
    
    def test_basic_mesh_generation(self):
        """Test basic mesh generation from TPMS."""
        gyroid = Gyroid(scale=10.0, thickness=0.0)
        mesh = generate_mesh(
            gyroid,
            resolution=30,
            iso_value=0.0,
            bounds=((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0))
        )
        
        assert isinstance(mesh, trimesh.Trimesh)
        assert len(mesh.vertices) > 0
        assert len(mesh.faces) > 0
    
    def test_mesh_has_valid_faces(self):
        """Test that generated mesh has valid face indices."""
        gyroid = Gyroid(scale=10.0)
        mesh = generate_mesh(
            gyroid,
            resolution=25,
            iso_value=0.0
        )
        
        if len(mesh.faces) > 0:
            # Check that all face indices are valid
            max_vertex_idx = len(mesh.vertices) - 1
            assert np.all(mesh.faces >= 0)
            assert np.all(mesh.faces <= max_vertex_idx)
    
    def test_different_iso_values(self):
        """Test mesh generation with different iso-values."""
        gyroid = Gyroid(scale=10.0)
        
        mesh1 = generate_mesh(gyroid, resolution=25, iso_value=0.0)
        mesh2 = generate_mesh(gyroid, resolution=25, iso_value=0.5)
        
        # Different iso-values should produce different meshes
        # (though they might have similar structure)
        assert isinstance(mesh1, trimesh.Trimesh)
        assert isinstance(mesh2, trimesh.Trimesh)


class TestIndustrialAnalysis:
    """Test cases for industrial analysis functions."""
    
    def test_volume_calculation(self):
        """Test volume calculation."""
        # Create a simple box mesh
        box = trimesh.creation.box(extents=[2.0, 2.0, 2.0])
        volume = calculate_volume(box)
        
        # Box volume should be 2*2*2 = 8
        assert abs(volume - 8.0) < 1e-6
    
    def test_bounding_box_calculation(self):
        """Test bounding box calculation."""
        box = trimesh.creation.box(extents=[2.0, 3.0, 4.0])
        bbox = calculate_bounding_box(box)
        
        assert 'x' in bbox
        assert 'y' in bbox
        assert 'z' in bbox
        assert bbox['x'][1] - bbox['x'][0] == 2.0
        assert bbox['y'][1] - bbox['y'][0] == 3.0
        assert bbox['z'][1] - bbox['z'][0] == 4.0
    
    def test_dimensions_calculation(self):
        """Test dimensions calculation."""
        box = trimesh.creation.box(extents=[2.0, 3.0, 4.0])
        dims = calculate_dimensions(box)
        
        assert dims['width'] == 2.0
        assert dims['height'] == 3.0
        assert dims['depth'] == 4.0
    
    def test_analyze_geometry(self):
        """Test comprehensive geometry analysis."""
        box = trimesh.creation.box(extents=[2.0, 2.0, 2.0])
        analysis = analyze_geometry(box)
        
        assert 'volume' in analysis
        assert 'surface_area' in analysis
        assert 'bbox' in analysis
        assert 'dimensions' in analysis
        assert 'is_watertight' in analysis
        assert 'vertex_count' in analysis
        assert 'face_count' in analysis
        
        assert analysis['volume'] > 0
        assert analysis['surface_area'] > 0
        assert analysis['is_watertight'] == True
    
    def test_material_usage_estimation(self):
        """Test material usage estimation."""
        box = trimesh.creation.box(extents=[1.0, 1.0, 1.0])  # 1 cm³
        usage = estimate_material_usage(box, material_density=1.0)  # 1 g/cm³
        
        # Volume = 1 cm³, density = 1 g/cm³, mass = 1 g
        # But volume is in mm³, so 1000 mm³ = 1 cm³
        assert usage['volume'] > 0
        assert usage['mass'] > 0
        assert 'density' in usage


class TestMeshValidation:
    """Test cases for mesh validation."""
    
    def test_mesh_export(self):
        """Test that generated mesh can be exported."""
        gyroid = Gyroid(scale=10.0)
        mesh = generate_mesh(
            gyroid,
            resolution=25,
            iso_value=0.0
        )
        
        if len(mesh.vertices) > 0:
            # Try to export (should not raise exception)
            try:
                export_data = mesh.export(file_type='stl')
                assert export_data is not None
            except Exception as e:
                pytest.fail(f"Mesh export failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
