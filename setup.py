# setup.py

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RackioModbus",
    version="0.2",
    author="Nelson Carrasquel",
    author_email="rackio.framework@outlook.com",
    description="A Rackio extension to enable Modbus TCP Server/Client integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/rack-io/rackio-modbus",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=[
        'umodbus',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
