"""
Setup script for ScatCluster
"""
from setuptools import find_packages, setup

NAME = 'scatcluster'
DESCRIPTION = 'A workflow for clustering continuous time series with a deep scattering network.'
URL = 'https://github.com/INGV/ScatCluster'
AUTHOR = 'christopher.zerafa@ingv.it'
REQUIRES_PYTHON = '>=3.8.0'
PYTHON_CODE_PREFIX = 'scatcluster'

REQUIRED = [
    'tqdm', 'obspy>=1.4.0', 'scatseisnet>=0.2.1', 'pandas', 'seaborn', 'fastcluster', 'scikit-learn==1.2.2', 'click',
    'nmmn', 'astropy', 'parse', 'scipy'
]

REQUIRED_GPU = [
    'cupy>=11.3.0',
]

setup(
    name=NAME,
    author=AUTHOR,
    version='0.0.84',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(where='.'),
    package_data={NAME: ['scatcluster/*.py']},
    include_package_data=True,
    install_requires=REQUIRED,
    extras_require={'gpu': [*REQUIRED, *REQUIRED_GPU]},
    license='MIT',
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
