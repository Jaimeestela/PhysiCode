"""
Triply Periodic Minimal Surfaces (TPMS)
Created by Jaime Estela | https://github.com/Jaimeestela | studio@jaimeestela.com

This module implements various TPMS surfaces, which are mathematical
surfaces that are periodic in three dimensions and minimize surface area
for a given volume. These surfaces are widely used in generative design
and lattice structures for additive manufacturing.
"""

import numpy as np
from typing import Union
from core.fields import ScalarField


class Gyroid(ScalarField):
    """
    Gyroid Triply Periodic Minimal Surface.
    
    The Gyroid is a continuous, triply periodic minimal surface discovered
    by Alan Schoen in 1970. It has applications in material science,
    architecture, and generative design.
    
    Mathematical definition:
        f(x, y, z) = sin(x) * cos(y) + sin(y) * cos(z) + sin(z) * cos(x)
    
    The iso-surface at f(x, y, z) = 0 defines the Gyroid surface.
    
    Attributes
    ----------
    scale : float
        Scaling factor for the periodic structure
    thickness : float
        Thickness parameter for creating solid volumes (default: 0.0)
        When thickness > 0, creates a solid with wall thickness
    
    Examples
    --------
    >>> gyroid = Gyroid(scale=10.0, thickness=0.5)
    >>> value = gyroid(1.0, 2.0, 3.0)
    >>> # Generate mesh at iso-value 0.0
    """
    
    def __init__(self, scale: float = 1.0, thickness: float = 0.0):
        """
        Initialize a Gyroid TPMS field.
        
        Parameters
        ----------
        scale : float, optional
            Scaling factor for the periodic structure, by default 1.0
        thickness : float, optional
            Thickness parameter for solid volumes, by default 0.0
        """
        super().__init__(scale=scale)
        self.thickness = thickness
    
    def evaluate(self, x: Union[float, np.ndarray], 
                 y: Union[float, np.ndarray], 
                 z: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Evaluate the Gyroid function at given coordinates.
        
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
            Gyroid function value(s)
        """
        # Core Gyroid equation
        value = (np.sin(x) * np.cos(y) + 
                 np.sin(y) * np.cos(z) + 
                 np.sin(z) * np.cos(x))
        
        # Apply thickness if specified
        if self.thickness > 0:
            # Create solid volume by offsetting the surface
            value = np.abs(value) - self.thickness
        
        return value


class SchwarzP(ScalarField):
    """
    Schwarz P (Primitive) Triply Periodic Minimal Surface.
    
    The Schwarz P surface is one of the first discovered TPMS surfaces,
    named after Hermann Schwarz who studied minimal surfaces in the 19th
    century. It has a cubic symmetry and is commonly used in lattice
    structures.
    
    Mathematical definition:
        f(x, y, z) = cos(x) + cos(y) + cos(z)
    
    The iso-surface at f(x, y, z) = 0 defines the Schwarz P surface.
    
    Attributes
    ----------
    scale : float
        Scaling factor for the periodic structure
    thickness : float
        Thickness parameter for creating solid volumes (default: 0.0)
    
    Examples
    --------
    >>> schwarz_p = SchwarzP(scale=8.0, thickness=0.3)
    >>> value = schwarz_p(1.0, 2.0, 3.0)
    """
    
    def __init__(self, scale: float = 1.0, thickness: float = 0.0):
        """
        Initialize a Schwarz P TPMS field.
        
        Parameters
        ----------
        scale : float, optional
            Scaling factor for the periodic structure, by default 1.0
        thickness : float, optional
            Thickness parameter for solid volumes, by default 0.0
        """
        super().__init__(scale=scale)
        self.thickness = thickness
    
    def evaluate(self, x: Union[float, np.ndarray], 
                 y: Union[float, np.ndarray], 
                 z: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Evaluate the Schwarz P function at given coordinates.
        
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
            Schwarz P function value(s)
        """
        # Core Schwarz P equation
        value = np.cos(x) + np.cos(y) + np.cos(z)
        
        # Apply thickness if specified
        if self.thickness > 0:
            # Create solid volume by offsetting the surface
            value = np.abs(value) - self.thickness
        
        return value
