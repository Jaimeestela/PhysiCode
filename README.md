# PhysiCode: Bridging Mathematical Theory and Industrial Production

<div align="center">

**Engineering-as-Code Toolkit for Mathematical Geometry, Industrial Optimization, and Generative Design**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-Interactive-orange.svg)](https://streamlit.io/)

</div>

---

## 🎯 Vision

**PhysiCode** democratizes high-end computational engineering by providing an open-source toolkit that transforms mathematical abstractions into manufacturable 3D geometry. This project bridges the gap between theoretical mathematics and industrial production, enabling designers, engineers, and researchers to generate complex geometries through code.

### What is Engineering-as-Code?

Engineering-as-Code is a paradigm where mathematical functions, physical constraints, and design parameters are expressed as executable code. This approach enables:

- **Reproducible Design**: Every geometry is generated from a mathematical definition
- **Parametric Optimization**: Iterate designs programmatically
- **Scalable Production**: Generate thousands of variations automatically
- **Mathematical Rigor**: Ensure geometric properties through formal definitions

---

## 👤 Author & Credits

**PhysiCode** is developed and maintained by **Jaime Estela**, a specialist in Industrial Design Engineering and Mathematical Computation.

- **GitHub**: [@Jaimeestela](https://github.com/Jaimeestela)
- **Contact**: studio@jaimeestela.com
- **License**: Apache License 2.0

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Interactive App

```bash
streamlit run app/main.py
```

The app will open in your browser, allowing you to:
- Select mathematical primitives (TPMS surfaces, distance fields, etc.)
- Adjust parameters in real-time (iso-value, resolution, scale)
- Visualize 3D geometry interactively
- Export results as STL files

### Step 3: Export Your First Geometry

1. Select a primitive (e.g., "Gyroid TPMS")
2. Adjust the sliders to your desired parameters
3. Click "Generate Geometry"
4. Download the STL file for 3D printing or CAD import

---

## 📁 Project Structure

```
PhysiCode/
├── core/                    # Mathematical foundations
│   ├── __init__.py
│   ├── fields.py           # Scalar field base classes
│   └── tpms.py             # Triply Periodic Minimal Surfaces
├── geometry/                # Mesh generation
│   ├── __init__.py
│   ├── marching_cubes.py   # Marching Cubes algorithm
│   └── industrial.py       # Volume, bounding box calculations
├── app/                     # Streamlit dashboard
│   ├── __init__.py
│   └── main.py             # Interactive playground
├── examples/                # Educational scripts
│   ├── basic_tpms.py
│   ├── custom_field.py
│   └── batch_export.py
├── tests/                   # Unit tests
│   ├── __init__.py
│   ├── test_fields.py
│   ├── test_tpms.py
│   └── test_geometry.py
├── LICENSE                  # Apache 2.0 License
├── NOTICE                   # Attribution notice
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

---

## 🔬 Core Features

### Mathematical Primitives

- **Scalar Fields**: Base class for defining 3D mathematical functions
- **TPMS Surfaces**: 
  - Gyroid surface
  - Schwarz P surface
  - Extensible architecture for additional surfaces
- **Distance Fields**: Signed distance functions for geometric operations

### Industrial Tools

- **Volume Calculation**: Accurate material volume estimation
- **Bounding Box Analysis**: Dimensional analysis for manufacturing
- **Mesh Validation**: Geometric integrity checks
- **STL/STEP Export**: Industry-standard file formats

### Interactive Playground

- Real-time parameter adjustment
- Live 3D visualization
- Instant STL export
- Parameter presets for common use cases

---

## 📚 Examples

### Basic TPMS Generation

```python
from core.tpms import Gyroid
from geometry.marching_cubes import generate_mesh
from geometry.industrial import analyze_geometry

# Create a Gyroid field
gyroid = Gyroid(scale=10.0, thickness=0.5)

# Generate mesh
mesh = generate_mesh(gyroid, resolution=50, iso_value=0.0)

# Analyze geometry
analysis = analyze_geometry(mesh)
print(f"Volume: {analysis['volume']:.2f} mm³")
print(f"Bounding Box: {analysis['bbox']}")
```

### Custom Scalar Field

```python
from core.fields import ScalarField
import numpy as np

class CustomField(ScalarField):
    def evaluate(self, x, y, z):
        return np.sin(x) * np.cos(y) * np.sin(z)

field = CustomField()
mesh = generate_mesh(field, resolution=40, iso_value=0.5)
```

See the `examples/` directory for more comprehensive examples.

---

## 🧪 Testing

Run the test suite to validate geometric operations:

```bash
pytest tests/
```

---

## 📖 Documentation

Each module includes comprehensive docstrings following NumPy style guidelines. Key concepts:

- **Scalar Fields**: Mathematical functions \(f(x, y, z) \rightarrow \mathbb{R}\)
- **Iso-surfaces**: Level sets where \(f(x, y, z) = c\)
- **Marching Cubes**: Algorithm for extracting triangular meshes from scalar fields

---

## 🤝 Contributing

Contributions are welcome! Please ensure:

1. Code follows PEP 8 style guidelines
2. All functions include docstrings
3. Tests are added for new features
4. Attribution header is maintained in source files

---

## 📄 License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

**Important**: Any redistribution of this software must include attribution to Jaime Estela as specified in the [NOTICE](NOTICE) file.

---

## 🔗 Links

- **GitHub Repository**: [https://github.com/Jaimeestela/PhysiCode](https://github.com/Jaimeestela/PhysiCode)
- **Author Profile**: [https://github.com/Jaimeestela](https://github.com/Jaimeestela)
- **Contact**: studio@jaimeestela.com

---

<div align="center">

**Made with ❤️ by Jaime Estela**

*Transforming Mathematics into Matter*

</div>
