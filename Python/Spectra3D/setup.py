import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spectra3D-i3DR", # Replace with your own username
    version="0.0.3.1",
    author="Ben Knight",
    author_email="bknight@i3drobotics.com",
    description="Adding spectrum to 3D",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/i3drobotics/Spectra3D",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy','matplotlib','mpl_toolkits',
        'plyfile','csv'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)