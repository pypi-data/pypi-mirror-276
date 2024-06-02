from CDPS.core.constants import core_constant

from setuptools import setup, find_packages

setup(
    name=core_constant.NAME,
    version=core_constant.VERSION,
    description='A simple example package',
    author='ExpTechTW',
    author_email='exptech.tw@gmail.com',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
)