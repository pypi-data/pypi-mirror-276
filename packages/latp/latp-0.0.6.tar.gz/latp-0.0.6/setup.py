# setup.py
# !/usr/bin/python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from latp import __description__, __version__, __pro_name__

# 读取 README 文件作为长描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=__pro_name__,
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Tanyu',
    author_email='cypenite@gmail.com',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    license='MIT',
    entry_points={
        'console_scripts': [
            'latp = latp.cli:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pytest',
        'pyyaml',
        'requests',
        'loguru',
    ],
    package_data={
        'latp': ['config.yaml'],
    },
)
