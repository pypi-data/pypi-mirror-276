# setup.py
from setuptools import setup, find_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='excel_normalizer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'normalize=excel_normalizer.cli:main',
        ],
    },
    install_requires=[
        'pandas',
        'pyarrow',
        'openpyxl'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

