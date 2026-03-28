from setuptools import setup, find_packages

setup(
    name="parser-products",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "selectolax>=0.3.0",
        "loguru>=0.7.0",
        "tqdm>=4.65.0",
    ],
    python_requires=">=3.8",
)