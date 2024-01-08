from setuptools import setup, find_packages

setup(
    name='ProjectileSim',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'ProjectileSim = simulator.py'
        ]
    },
)