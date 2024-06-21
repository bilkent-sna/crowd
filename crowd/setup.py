from setuptools import setup, find_packages

from setuptools.command.install import install

setup(
    name="crowd",
    version="0.1",
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
    	
    author="Tolga Yilmaz",
    description="Crowd:a social network simulation framework",
    keywords="social networks, network, simulation",
    url=""
)