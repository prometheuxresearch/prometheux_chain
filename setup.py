from setuptools import setup, find_packages

setup(
    name="prometheux_chain",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyyaml",
        "pandas",
        "networkx"
    ],
    package_data={
        'prometheux_chain': ['config.yaml'],
    },
    include_package_data=True,
    author='Prometheux Limited',
    author_email='davben@prometheux.co.uk',
    description='Prometheux chain is a Python SDK designed to build, evolve and deploy your new knowledge graphs.',
    long_description=open('ReadMe.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/prometheuxresearch/prometheux_chain',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
