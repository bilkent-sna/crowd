from setuptools import setup, find_packages

from setuptools.command.install import install

setup(
    name="crowd",
    version="0.9",
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.txt']},
    install_requires=[
        "pandas",
        "networkx",
        "pyyaml",
        "python-louvain",
        "imageio",
        "matplotlib",
        "ndlib"
    ],
    	
    author="Tolga Yilmaz, Nese Rende",
    description="Crowd:a social network simulation framework",
    keywords="social networks, network, simulation",
    url="https://github.com/Bilkent-Social-Systems-Research-Group/crowd/"
)