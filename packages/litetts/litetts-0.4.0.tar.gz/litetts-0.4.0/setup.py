# setup.py
from setuptools import setup, find_packages

setup(
    name="litetts",
    version="0.4.0",
    author="Md Rehan",
    author_email="mdrehan4all@gmail.com",
    description="A package to convert text into speech",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mdrehan4all/litetts",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pyobjc (>=2.4); platform_system == "Darwin"',
        'comtypes ; platform_system == "Windows"',
        'pypiwin32 ; platform_system == "Windows"',
        'pywin32 ; platform_system == "Windows"',
    ],
    python_requires='>=3.6',
)