"""
Scalar Field Base Classes
Created by Jaime Estela | https://github.com/Jaimeestela | studio@jaimeestela.com

This module defines the abstract base class for scalar fields, which are
mathematical functions f(x, y, z) -> R that map 3D coordinates to real values.
"""

import numpy as np
from abc import ABC, abstractmethod
from typing import Union, Tuple


class ScalarField(ABC):
    """
    Abstract base class for scalar fields in 3D space.
    
    A scalar field is a mathematical function that assigns a real number
    to each point in 3D space: f(x, y, z) -> R
    
    Subclasses must implement the evaluate method to define the specific
    mathematical function.
    
    Attributes
    ----------
    scale : float
        Scaling factor for the field (default: 1.0)
    offset : tuple of float
        Translation offset (x, y, z) for the field (default: (0, 0, 0))
    
    Examples
    --------
    >>> class CustomField(ScalarField):
    ...     def evaluate(self, x, y, z):
    ...         return np.sin(x) * np.cos(y)
    >>> field = CustomField(scale=2.0)
    >>> value = field(1.0, 2.0, 3.0)
    """
    
    def __init__(self, scale: float = 1.0, offset: Tuple[float, float, float] = (0.0, 0.0, 0.0)):
        """
        Initialize a scalar field.
        
        Parameters
        ----------
        scale : float, optional
            Scaling factor for the field coordinates, by default 1.0
        offset : tuple of float, optional
            Translation offset (x, y, z), by default (0.0, 0.0, 0.0)
        """
        self.scale = scale
        self.offset = np.array(offset, dtype=np.float64)
    
    @abstractmethod
    def evaluate(self, x: Union[float, np.ndarray], 
                 y: Union[float, np.ndarray], 
                 z: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Evaluate the scalar field at given coordinates.
        
        This method must be implemented by subclasses to define the
        specific mathematical function.
        
        Parameters
        ----------
        x : float or np.ndarray
            X coordinates
        y : float or np.ndarray
            Y coordinates
        z : float or np.ndarray
            Z coordinates
        
        Returns
        -------
        float or np.ndarray
            Scalar field value(s) at the given coordinates
        """
        pass
    
    def __call__(self, x: Union[float, np.ndarray], 
                 y: Union[float, np.ndarray], 
                 z: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Evaluate the scalar field with scaling and offset applied.
        
        Parameters
        ----------
        x : float or np.ndarray
            X coordinates
        y : float or np.ndarray
            Y coordinates
        z : float or np.ndarray
            Z coordinates
        
        Returns
        -------
        float or np.ndarray
            Scalar field value(s) at the transformed coordinates
        """
        # Apply scaling and offset
        x_scaled = x * self.scale + self.offset[0]
        y_scaled = y * self.scale + self.offset[1]
        z_scaled = z * self.scale + self.offset[2]
        
        return self.evaluate(x_scaled, y_scaled, z_scaled)
    
    def evaluate_grid(self, x_range: Tuple[float, float], 
                     y_range: Tuple[float, float],
                     z_range: Tuple[float, float],
                     resolution: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Evaluate the scalar field on a regular 3D grid.
        
        Parameters
        ----------
        x_range : tuple of float
            (x_min, x_max) range for X coordinates
        y_range : tuple of float
            (y_min, y_max) range for Y coordinates
        z_range : tuple of float
            (z_min, z_max) range for Z coordinates
        resolution : int
            Number of points along each axis
        
        Returns
        -------
        tuple of np.ndarray
            (coordinates, values) where:
            - coordinates: (N, 3) array of (x, y, z) points
            - values: (N,) array of scalar field values
        """
        x = np.linspace(x_range[0], x_range[1], resolution)
        y = np.linspace(y_range[0], y_range[1], resolution)
        z = np.linspace(z_range[0], z_range[1], resolution)
        
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        coords = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1)
        
        values = self(X.ravel(), Y.ravel(), Z.ravel())
        
        return coords, values
