# AI_plug-in_1/setup.py
from setuptools import setup, find_packages

setup(
    name='AI_plug_in_1',
    version='0.2',
    packages=find_packages(),
    # package_data={'': ['*.json', '*.txt']},  # Include non-Python files
    exclude_package_data={'': ['*.py']},     # Exclude Python files
)