from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()


# Function to read the contents of your requirements file
def read_requirements():
    with open('requirements.txt') as req:
        return req.read().splitlines()


setup(
    name="WaveyMcWaveFace",
    version="1.0",
    description="A quick way to run Google's TiDE model",
    package_dir={"": "TiDE"},
    packages=find_packages(where="TiDE"),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/AmwayCommon/wavey",
    author="Jordan Howell",
    author_email="jordan.howell@amway.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    install_requires=read_requirements(),
    extras_require={"dev": ["pytest==8.2.1", "twine==5.1.0"]},
    python_requires=">=3.10"
    )
