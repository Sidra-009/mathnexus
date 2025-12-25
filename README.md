<<<<<<< HEAD
# MathNexus: Mathematical Framework 📐🚀

[![PyPI version](https://badge.fury.io/py/mathnexus.svg)](https://badge.fury.io/py/mathnexus)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

**MathNexus** is a modular, object-oriented Python framework that provides a clean and intuitive implementation of **Linear Algebra** and **Analytical (Coordinate) Geometry**.  
It is designed with **learning, correctness, and extensibility** in mind — exposing how mathematical concepts translate into real software systems.

Unlike traditional numerical libraries that abstract away the internal logic, MathNexus focuses on **clarity over black-box computation**, making it especially suitable for:
- Students learning mathematics + programming
- Educators demonstrating mathematical modeling
- Developers building simulation or geometry-based tools

---
***UNDER MAINTENANCE***
=======
# CleanCore

CleanCore is a **dependency-free data transformation audit framework**.

Unlike data profilers, CleanCore tracks:
- What changed
- Which rows were affected
- Before / after values
- Why it changed (business rule)
- Compliance-ready audit trail

## Example

```python
from cleancore import CleanEngine, print_audit_report

engine = CleanEngine(df)
cleaned_df, audit_log = engine.run()
print_audit_report(audit_log)
>>>>>>> 1db3dbe (Replace mathnexus with CleanCore audit framework)
