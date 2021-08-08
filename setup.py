from setuptools import setup, find_packages
from minesweeper import __version__

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = ''

setup(
    name='ascii-minesweeper',
    version=__version__,
    author='Nathaniel Young',
    author_email='',
    url='https://github.com/nyoungstudios/ascii-minesweeper',
    description='An interactive minesweeper game for your terminal.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'minesweeper = minesweeper.run:main'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords='minesweeper ascii ascii-art terminal game python',
    install_requires=requirements
)
