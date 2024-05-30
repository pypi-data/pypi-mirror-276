from setuptools import setup, find_packages

setup(
    name="mem-client",
    version="0.0.1",
    description="A Python client for interacting with the Mem API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/elviiai/mem-client",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "python-dotenv>=0.19.2",
        "click>=8.0.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
