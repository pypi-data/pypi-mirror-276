from setuptools import find_packages, setup

PACKAGE = "hapitools"

VERSION = "0.1.0"

with open("README.md", "r") as fh:
    long_description = fh.read()
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name=PACKAGE,
    version=VERSION,
    author="icehapi",
    author_email="icehapi@163.com",
    description="My python tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/icehapi/hapitools",
    packages=find_packages(),
    include_package_data=True,
    data_files=["requirements.txt"],
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.8',
    install_requires=required,
)