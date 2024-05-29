# setup.py

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="wealthwatchdog",
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # Add any dependencies your library needs
    author="Jammulapati Ravi Teja",
    author_email="ravitejajammulapti@gmail.com",
    description="A personal finance calculator library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RaviTejaJp/WealthWatchDog.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
