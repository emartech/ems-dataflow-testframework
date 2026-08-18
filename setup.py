import setuptools

__version__ = "1.4.0"

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="ems-dataflow-testframework",
    version=__version__,
    author="Emarsys",
    description="Framework helping testing Google Cloud Dataflows",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests", "test_.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "attrs>=23.1.0",
        "cachetools>=5.3.0",
        "ems-gcp-toolkit==0.2.2",
        "google-auth>=2.0.0",
        "google-cloud-bigtable>=2.0.0",
        "grpcio>=1.59.0",
        "inflection>=0.5.1",
        "packaging>=23.0",
        "pluggy>=1.0.0",
        "protobuf>=4.25.0",
        "pytest>=7.0.0",
        "pytz>=2023.3",
        "requests>=2.31.0",
        "six>=1.16.0",
        "tenacity>=8.2.0",
    ]
)
