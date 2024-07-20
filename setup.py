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
    entry_points={
        'console_scripts': [
            'prometheux=prometheux_chain.__main__:main'
        ],
    },
)
