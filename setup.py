import os
from setuptools import setup, find_packages

# Read version from version.txt
with open("version.txt", "r") as f:
    version = f.read().strip()
    
# Get the directory where setup.py is located
this_directory = os.path.abspath(os.path.dirname(__file__))

# Read the contents of ReadMe.md
with open(os.path.join(this_directory, 'ReadMe.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="prometheux_chain",
    version=version,
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyyaml",
        "pandas",
        "networkx",
        "pyvis",
        "ipycytoscape",
        "matplotlib"
    ],
    package_data={
        'prometheux_chain': ['config.yaml'],
    },
    include_package_data=True,
    author='Prometheux Limited',
    author_email='davben@prometheux.co.uk',
    description='Prometheux chain is a Python SDK designed to build, evolve and deploy your new knowledge graphs.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/prometheuxresearch/prometheux_chain',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
)
