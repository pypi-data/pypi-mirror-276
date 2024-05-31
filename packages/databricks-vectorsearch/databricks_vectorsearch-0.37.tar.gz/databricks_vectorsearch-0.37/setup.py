import os
from setuptools import find_packages, setup
from importlib.machinery import SourceFileLoader

with open("requirements.txt") as f:
    required = f.read().splitlines()

version = (
    SourceFileLoader(
        "version", os.path.join("databricks", "vector_search", "version.py")
    )
    .load_module()
    .VERSION
)

setup(
    name="databricks_vectorsearch",
    version=version,
    packages=find_packages(),
    author="Databricks",
    author_email="feedback@databricks.com",
    license_files=("LICENSE.md"),
    description="Databricks Vector Search Client",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=required,
    python_requires=">=3.7",
)
