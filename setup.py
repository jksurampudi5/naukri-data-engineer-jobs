from setuptools import setup, find_packages

setup(
    name="naukri-data-engineer-jobs",
    version="1.0.0",
    description="Naukri Data Engineer Jobs Ingestion & Market Analytics Pipeline",
    packages=find_packages(),
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "naukri-de=src.naukri_de.cli:main",
        ],
    },
)
