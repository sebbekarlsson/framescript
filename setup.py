from setuptools import setup, find_packages


setup(
    name='jscomp',
    version='1.0.0',
    install_requires=[
        'termcolor',
        'jsbeautifier',
        'bs4'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'jscomp = jscomp.bin:run'
        ]
    }
)
