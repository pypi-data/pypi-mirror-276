from distutils.core import setup
from setuptools import find_packages


version = "0.0.1"
# Extract version from CHANGES.md
with open("./CHANGES.md", "r") as file:
        for line in file:
            if line.strip():
                version = line.strip()
                break


setup(
    name="functionize-notebook",
    version=version,
    author="Bui Hoang Tu",
    author_email="bhtu.work@gmail.com",
    url="https://github.com/BuiHoangTu/functionize-notebook/",
    license="MIT",
    packages=find_packages(),
    package_dir={"notebook_wrapper": "notebook_wrapper"},
    description="run notebook like a function",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["nbformat", "nbconvert", "ipykernel", "dill"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
)
