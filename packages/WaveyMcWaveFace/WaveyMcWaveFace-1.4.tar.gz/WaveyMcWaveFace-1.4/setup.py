from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

packages = find_packages()
print(f"Packages found: {packages}")

setup(
    name="WaveyMcWaveFace",
    version="1.4",
    license='MIT',
    description="A quick way to run Google's WaveyMcWaveFace model",
    package_dir={'WaveyMcWaveFace': 'WaveyMcWaveFace'},
    packages=packages,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/AmwayCommon/wavey",
    author="Jordan Howell",
    author_email="jordan.howell@amway.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    install_requires=['pandas',
                      'pandas-profiling',
                      'pandocfilters',
                      'numpy',
                      'scikit-learn',
                      'torch'],
    extras_require={"dev": ["pytest==8.2.1", "twine==5.1.0"]},
    python_requires=">=3.10"
    )
