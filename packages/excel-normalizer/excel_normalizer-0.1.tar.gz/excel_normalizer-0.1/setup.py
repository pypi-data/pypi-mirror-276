# setup.py
from setuptools import setup, find_packages

setup(
    name='excel_normalizer',
    version='0.1',
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

