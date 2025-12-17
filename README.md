# MathNexus: Advanced Mathematical Framework 📐🚀

[![PyPI version](https://badge.fury.io/py/mathnexus.svg)](https://badge.fury.io/py/mathnexus)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

**MathNexus** is a modular, object-oriented Python framework that provides a clean and intuitive implementation of **Linear Algebra** and **Analytical (Coordinate) Geometry**.  
It is designed with **learning, correctness, and extensibility** in mind — exposing how mathematical concepts translate into real software systems.

Unlike traditional numerical libraries that abstract away the internal logic, MathNexus focuses on **clarity over black-box computation**, making it especially suitable for:
- Students learning mathematics + programming
- Educators demonstrating mathematical modeling
- Developers building simulation or geometry-based tools

---

## ✨ Design Philosophy

MathNexus follows three core principles:

1. **Mathematics as Datatypes**  
   Vectors, matrices, points, and lines are treated as *first-class objects*, not raw lists or tuples.

2. **Readable over Magical**  
   Every operation mirrors the mathematical definition closely, allowing learners to trace formulas directly into code.

3. **Pure Python, Zero Dependencies**  
   No NumPy, no SciPy — everything is implemented from scratch using OOP fundamentals.

---

## 📊 Core Modules & Capabilities

| Module | Description | Concepts Covered |
|------|------------|------------------|
| **`coordinate_geometry`** | Analytical & Euclidean geometry | Points, lines, distances, slopes, midpoints, shapes |
| **`linear_datatypes`** | Linear algebra foundations | Vectors, matrices, norms, dot products |
| **`physics_visuals`** | Simulation bridge (future) | Geometry-to-visualization interface |

---

## 🧬 Mathematical Foundations

### 1. Coordinate Geometry 📍

MathNexus implements classical Euclidean geometry using mathematically accurate formulas.

**Distance Formula (2D):**

\[
d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}
\]

**Example:**
```python
from mathnexus.coordinate_geometry import calculate_distance

p1 = (0, 0)
p2 = (3, 4)

print(calculate_distance(p1, p2))  # 5.0
```

Learners can easily verify the formula step-by-step within the source code.

---

### 2. Vector Algebra 🔢

Vectors are implemented as a **custom datatype**, supporting common linear algebra operations without relying on external libraries.

**Vector Magnitude (L² Norm):**

\[
\| \mathbf{v} \| = \sqrt{\sum_{i=1}^n v_i^2}
\]

**Example:**
```python
from mathnexus.linear_datatypes import Vector

v = Vector(5, 12)
print(v.magnitude())  # 13.0
```

Additional vector operations include:
- Vector addition
- Dot product
- Normalization
- Dimension checks with meaningful error messages

---

## 📘 Beginner-Friendly API Documentation

### 📐 coordinate_geometry

| Function | Description |
|--------|------------|
| `calculate_distance(p1, p2)` | Returns Euclidean distance between two points |
| `calculate_slope(p1, p2)` | Computes slope of a line segment |
| `get_midpoint(p1, p2)` | Returns midpoint of two coordinates |

---

### 🔢 linear_datatypes

#### Vector
```python
Vector(*components)
```

**Methods:**
- `.magnitude()` → Length of the vector  
- `.normalize()` → Unit vector in same direction  
- `.dot(other)` → Dot product  
- `.add(other)` → Vector addition  

#### Matrix
- Matrix addition
- Matrix multiplication
- Transpose
- Shape validation & error handling

---

## 🛠 Project Structure

```text
mathnexus/
├── coordinate_geometry/    # Geometric primitives & validation
├── linear_datatypes/       # Vector & Matrix datatypes
├── physics_visuals/        # Simulation-ready interfaces (planned)
└── tests/                  # Unit tests & edge cases
```

---

## 🎯 Who Is This Library For?

MathNexus is ideal for:
- Students learning **Linear Algebra & Geometry**
- Beginners practicing **OOP through math**
- Physics & engineering simulations
- Developers who want **transparent math logic**

It is **not meant to replace NumPy**, but to *teach and model mathematics correctly*.

---

## 🧪 Testing & Reliability

The library includes:
- Input validation
- Degenerate case handling (e.g., collinear points, zero-length vectors)
- Clear, descriptive exceptions for learning purposes

---

## 🤝 Contributions & Research Use

Contributions are welcome, especially in:
- 3D geometry extensions
- Optimized matrix algorithms
- Visualization support (Matplotlib, Unity, WebGL)

If used for academic or educational work, please cite the repository.

---

## 👩‍💻 Core Developer

**Sidra Saqlain**  

> *This project was built by debugging deeply, understanding failures,  
> and translating mathematical theory into clean, working code.*
