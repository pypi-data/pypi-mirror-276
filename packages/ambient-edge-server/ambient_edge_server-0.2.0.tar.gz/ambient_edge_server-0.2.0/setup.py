# setup.py
from setuptools import setup, find_packages

PACKAGE_NAME = 'ambient_edge_server'
VERSION = '0.2.0'

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        'fastapi==0.111.0',
        'pydantic==2.7.1',
        'ambient_event_bus_client==0.1.6',
        'ambient_backend_api_client==0.1.11',
        'setuptools==69.5.1',
        'pydantic_settings==2.2.1',
        'aiohttp==3.9.5',
        'cryptography==42.0.7',
        'async-lru==2.0.4',
        'result==0.16.1',
        'websockets==12.0',
        'docker==7.1.0',
    ],
    entry_points={
        'console_scripts': [
            'ambient_edge_server=ambient_edge_server.run:run',
        ],
    },
)
