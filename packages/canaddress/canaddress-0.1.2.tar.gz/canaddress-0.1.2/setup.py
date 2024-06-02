from setuptools import setup, find_packages

setup(
    name="canaddress",
    version="0.1.2",
    description="A library for cleaning and parsing addresses.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/avneeshchaudhary/canaddress",
    author="Avneesh Chaudhary",
    author_email="hey@avneeshchaudhary.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "openpyxl"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
