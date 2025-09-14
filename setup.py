from setuptools import setup, find_packages

setup(
    name="punnyland",
    version="1.0.0",
    description="A whimsical CLI for dad jokes with personality!",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.0",
        "colorama>=0.4.6",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "punnyland=punnyland.cli:main",
        ],
    },
    python_requires=">=3.7",
)