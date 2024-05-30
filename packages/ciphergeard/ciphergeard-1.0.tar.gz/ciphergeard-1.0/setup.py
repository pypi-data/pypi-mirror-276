import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ciphergeard",
    version="1.0",
    author="Evscion",
    author_email="ivoscev@gmail.com",
    description="Implementation of several famous ancient ciphers in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Evscion/Ciphergeard",
    download_url='https://github.com/Evscion/Ciphergeard/archive/refs/tags/v1.0.tar.gz',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    license_files=('LICENSE',),
    keywords=['cipher', 'encoder']
)