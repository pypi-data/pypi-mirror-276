from setuptools import setup, find_packages

__version__ = "2.1.1"

setup(
    name="request_api_builder",
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'requests',
        'chardet',
        'os',
    ],
)
