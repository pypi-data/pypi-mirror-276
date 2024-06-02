from setuptools import setup, find_packages

setup(
    name = "Lanes",
    author="SeaMite43981045",
    version="1.0.3",
    packages=find_packages(),
    py_modules='lanes.py',
    data_file='templates/TempNoFound.html',
    include_package_data=True,
    package_data={
        '':['*.html'],
    }
)