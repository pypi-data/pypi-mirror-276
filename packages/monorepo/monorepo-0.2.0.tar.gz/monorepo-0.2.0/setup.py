from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()


setup(
    name="monorepo",
    version="0.2.0",
    description="Import packages and modules from the root of a monorepo",
    url="https://github.com/myleott/monorepo",
    long_description = readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    packages=find_packages(),
)
