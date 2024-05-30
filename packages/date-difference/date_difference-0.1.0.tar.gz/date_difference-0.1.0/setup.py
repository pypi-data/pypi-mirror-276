from setuptools import setup, find_packages

setup(
    name="date_difference",
    version="0.1.0",
    description="A Python library to calculate the difference between two dates.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="devlopment-new10",
    author_email="githubuser16@gmail.com",
    url="https://github.com/gihubuser72/date_difference.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)