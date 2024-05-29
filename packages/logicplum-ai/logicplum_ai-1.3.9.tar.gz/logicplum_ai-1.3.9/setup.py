from setuptools import setup, find_packages
import os
# Get the absolute path of the current script
current_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(current_dir, "CHANGELOG.md"), "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='logicplum-ai',
    version='1.3.9',  # Update the version number
    packages=find_packages(),
    install_requires=[
        'requests',
        'Pillow'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)