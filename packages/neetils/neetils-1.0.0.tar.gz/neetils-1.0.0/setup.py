import os

from setuptools import find_packages, setup

with open("readme.md", "r", encoding="utf-8") as f:
    long_description = f.read()

requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
setup(name="neetils",
      version="v1.0.0",
      author="tanknee",
      author_email="nee@tanknee.cn",
      description="A package for tools",
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(include=["neetils", "neetils.*"]),
      install_requires=open(requirements_path).readlines())