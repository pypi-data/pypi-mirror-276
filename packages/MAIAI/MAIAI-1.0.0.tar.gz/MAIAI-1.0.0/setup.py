from setuptools import setup, find_packages

setup(
    name="MAIAI",
    version="1.0.0",
    description="A package to make working with AI simple.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Mikemaii/MAIAI",  # Update with your actual repository URL
    author="MikeMai",
    author_email="mike.maiyoulian@gmail.com",
    packages=find_packages(),
    install_requires=[
        "openai",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)