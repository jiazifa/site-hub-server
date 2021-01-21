from setuptools import find_packages, setup
import os

HERE = os.path.dirname(__name__)

setup(
    name="site-hub-server",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
