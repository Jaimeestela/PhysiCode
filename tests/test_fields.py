"""
Unit Tests for Scalar Fields
Created by Jaime Estela | https://github.com/Jaimeestela | studio@jaimeestela.com
"""

import pytest
import numpy as np
from core.fields import ScalarField


class TestScalarField(ScalarField):
    """Test implementation of ScalarField."""
    
    def evaluate(self, x, y, z):
        return x + y + z


class TestScalarFieldBase:
    """Test cases for ScalarField base class."""
    
    def test_basic_evaluation(self):
        """Test basic field evaluation."""
        field = TestScalarField()
        assert field(1.0, 2.0, 3.0) == 6.0
    
    def test_array_evaluation(self):
        """Test field evaluation with arrays."""
        field = TestScalarField()
        x = np.array([1.0, 2.0])
        y = np.array([1.0, 2.0])
        z = np.array([1.0, 2.0])
        result = field(x, y, z)
        expected = np.array([3.0, 6.0])
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_scale_parameter(self):
        """Test scaling parameter."""
        field = TestScalarField(scale=2.0)
        # With scale=2, (1,1,1) becomes (2,2,2) -> 6
        assert field(1.0, 1.0, 1.0) == 6.0
    
    def test_offset_parameter(self):
        """Test offset parameter."""
        field = TestScalarField(offset=(1.0, 1.0, 1.0))
        # With offset, (0,0,0) becomes (1,1,1) -> 3
        assert field(0.0, 0.0, 0.0) == 3.0
    
    def test_grid_evaluation(self):
        """Test grid evaluation."""
        field = TestScalarField()
        coords, values = field.evaluate_grid(
            x_range=(-1.0, 1.0),
            y_range=(-1.0, 1.0),
            z_range=(-1.0, 1.0),
            resolution=5
        )
        
        assert coords.shape == (125, 3)  # 5^3 = 125
        assert values.shape == (125,)
        assert len(coords) == len(values)


if __name__ == "__main__":
    pytest.main([__file__])
