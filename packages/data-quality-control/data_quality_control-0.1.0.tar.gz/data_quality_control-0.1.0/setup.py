# !/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='data_quality_control',
    packages=['fun', 'src'],
    version='0.1.0',
    description="Python code to perform data quality control on wind energy data, especially meteorological data",
    author="Ashim Giyanani",
    license="BSD License",
    author_email="ashimgiyanani@yahoo.com",
    url='https://github.com/ashimgiyanani/data_quality_control',
    download_url="https://github.com/ashimgiyanani/data_quality_control/archive/refs/tags/v0.1.0.tar.gz",
    keywords=['python', 'qualitycontrol', 'lidar', 'windenergy'],
    install_requires=[
        'pytest',
        'os', 'sys',
        'numpy', 'pandas',
        'matplotlib',
        'datetime',
    ],
    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Scientific/Engineering :: Atmospheric Science',
    'License :: OSI Approved :: BSD License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
    python_requires='>=3.9',
)
