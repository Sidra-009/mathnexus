from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="provena",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A dependency-free audit trail system for data transformations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/provena",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
    ],
    python_requires=">=3.7",
    install_requires=[],  # NO DEPENDENCIES - Pure Python!
    entry_points={
        "console_scripts": [
            "provena=provena.cli:main",
        ],
    },
    keywords="audit, logging, data-transformation, provenance, compliance",
)