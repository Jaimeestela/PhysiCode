"""
Unit Tests for TPMS Surfaces
Created by Jaime Estela | https://github.com/Jaimeestela | studio@jaimeestela.com
"""

import pytest
import numpy as np
from core.tpms import Gyroid, SchwarzP


class TestGyroid:
    """Test cases for Gyroid TPMS."""
    
    def test_basic_evaluation(self):
        """Test basic Gyroid evaluation."""
        gyroid = Gyroid(scale=1.0, thickness=0.0)
        value = gyroid.evaluate(0.0, 0.0, 0.0)
        # At origin, Gyroid = sin(0)*cos(0) + sin(0)*cos(0) + sin(0)*cos(0) = 0
        assert abs(value) < 1e-10
    
    def test_periodicity(self):
        """Test that Gyroid is periodic."""
        gyroid = Gyroid(scale=1.0, thickness=0.0)
        period = 2 * np.pi
        
        v1 = gyroid.evaluate(0.0, 0.0, 0.0)
        v2 = gyroid.evaluate(period, period, period)
        
        # Should be approximately equal due to periodicity
        assert abs(v1 - v2) < 1e-10
    
    def test_thickness_parameter(self):
        """Test thickness parameter."""
        gyroid_thin = Gyroid(scale=1.0, thickness=0.0)
        gyroid_thick = Gyroid(scale=1.0, thickness=0.5)
        
        # At same point, thick version should have different value
        x, y, z = 1.0, 1.0, 1.0
        v1 = gyroid_thin.evaluate(x, y, z)
        v2 = gyroid_thick.evaluate(x, y, z)
        
        # Thick version applies abs() and subtracts thickness
        assert v2 != v1
    
    def test_scale_parameter(self):
        """Test scale parameter."""
        gyroid_small = Gyroid(scale=1.0)
        gyroid_large = Gyroid(scale=2.0)
        
        # Same input coordinates, different scales
        v1 = gyroid_small(1.0, 1.0, 1.0)
        v2 = gyroid_large(1.0, 1.0, 1.0)
        
        # Should be different due to scaling
        assert v1 != v2
    
    def test_array_evaluation(self):
        """Test array evaluation."""
        gyroid = Gyroid(scale=1.0)
        x = np.array([0.0, np.pi/2, np.pi])
        y = np.array([0.0, np.pi/2, np.pi])
        z = np.array([0.0, np.pi/2, np.pi])
        
        values = gyroid(x, y, z)
        assert values.shape == (3,)


class TestSchwarzP:
    """Test cases for Schwarz P TPMS."""
    
    def test_basic_evaluation(self):
        """Test basic Schwarz P evaluation."""
        schwarz = SchwarzP(scale=1.0, thickness=0.0)
        value = schwarz.evaluate(0.0, 0.0, 0.0)
        # At origin, Schwarz P = cos(0) + cos(0) + cos(0) = 3
        assert abs(value - 3.0) < 1e-10
    
    def test_periodicity(self):
        """Test that Schwarz P is periodic."""
        schwarz = SchwarzP(scale=1.0, thickness=0.0)
        period = 2 * np.pi
        
        v1 = schwarz.evaluate(0.0, 0.0, 0.0)
        v2 = schwarz.evaluate(period, period, period)
        
        # Should be equal due to periodicity
        assert abs(v1 - v2) < 1e-10
    
    def test_thickness_parameter(self):
        """Test thickness parameter."""
        schwarz_thin = SchwarzP(scale=1.0, thickness=0.0)
        schwarz_thick = SchwarzP(scale=1.0, thickness=0.5)
        
        x, y, z = 1.0, 1.0, 1.0
        v1 = schwarz_thin.evaluate(x, y, z)
        v2 = schwarz_thick.evaluate(x, y, z)
        
        assert v2 != v1
    
    def test_iso_surface_property(self):
        """Test that iso-surface at 0 is meaningful."""
        schwarz = SchwarzP(scale=1.0, thickness=0.0)
        
        # At points where cos(x) + cos(y) + cos(z) = 0
        # This should create a valid surface
        x, y, z = np.pi/2, np.pi/2, np.pi/2
        value = schwarz.evaluate(x, y, z)
        # cos(π/2) = 0, so sum = 0
        assert abs(value) < 1e-10


if __name__ == "__main__":
    pytest.main([__file__])
