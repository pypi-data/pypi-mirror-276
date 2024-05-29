from setuptools import setup, find_packages

setup(
    name="modular-ai",  # New unique project name
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
    ],
    include_package_data=True,
    description="A library for interacting with various AI models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="HarveyGW",
    author_email="your_email@example.com",
    url="https://github.com/HarveyGW/AILib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
