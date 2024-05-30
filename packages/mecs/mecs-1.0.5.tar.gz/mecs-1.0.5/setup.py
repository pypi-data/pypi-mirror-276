from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name="mecs",
    version="1.0.5",
    packages=find_packages(),
    setup_requires=["setuptools", "wheel"],
    install_requires=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Library for stemming Madurese text",
)
