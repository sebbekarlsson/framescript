from setuptools import setup, find_packages


setup(
    name='framescript',
    version='1.0.0',
    install_requires=[
        'termcolor',
        'bs4',
        'jinja2',
        'jsmin',
        'htmlmin'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'framescript = framescript.bin:run'
        ]
    }
)
