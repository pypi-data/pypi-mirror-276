from setuptools import setup, find_packages
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


if sys.version_info < (3, 9):
    install_requires = [
        "grpcio==1.39.0",
        "grpcio-tools==1.39.0",
        "protobuf==3.17.3",
        "requests==2.22.0",
        "Pillow==9.5.0",
        "numpy==1.21.6",
        "pyModbusTCP==0.2.1",
        "netifaces==0.11.0"
    ]
else:
    install_requires = [
        "grpcio",
        "grpcio-tools",
        "protobuf",
        "requests",
        "Pillow",
        "numpy",
        "pyModbusTCP",
        "netifaces"
    ]

setup(
    name="neuromeka",
    version="3.2.0.2",
    author="Neuromeka",
    author_email="youngjin.heo@neuromeka.com",
    description="Neuromeka client protocols for IndyDCP3, IndyEye, Moby, Ecat, and Motor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neuromeka-robotics/neuromeka-clients3",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    python_requires=">=3.6",
    install_requires=install_requires,
)