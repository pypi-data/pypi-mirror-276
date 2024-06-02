from setuptools import setup, find_packages

setup(
    name="diamond-hpc",
    version="0.0.5",
    author="Haotian XIE, Gengcong YANG",
    author_email="hotinexie@gmail.com",
    description="Diamond is a Python package for running tasks on HPC.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Diamond-Proj/Diamond",
    packages=find_packages(),
    package_data={
        "diamond": ["diamond_client/templates/*"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "click>=8.1.3",
        "globus_compute_sdk>=2.20.0",
        "Jinja2>=3.1.4",
        "Requests>=2.32.2",
    ],
    entry_points={
        'console_scripts': [
            'diamond-hpc=diamond.wrapper.wrapper:cli',
        ],
    },
    python_requires='>=3.8',
)
