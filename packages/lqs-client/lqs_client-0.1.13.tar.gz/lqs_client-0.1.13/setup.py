import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lqs-client",
    version="0.1.13",
    author="Nathan Margaglio",
    author_email="nmargaglio@carnegierobotics.com",
    description="LogQS Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carnegierobotics/LogQS-Client",
    project_urls={
        "Bug Tracker": "https://github.com/carnegierobotics/LogQS-Client/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    packages=[
        "lqs_client",
        "lqs_client.interface",
        "lqs_client.gen",
        "lqs_client.definitions",
    ],
    python_requires=">=3.6",
    install_requires=[
        "fire>=0.4.0,<1.0",
        "python-dotenv>=0.0,<1.0",
        "requests>=2.0,<3.0",
        "xmltodict>=0.13.0,<1.0.0",
        "py3rosmsgs>=1.18.0,<2.0.0",
        "rospkg>=1.4.0,<2.0.0",
        "tqdm>=4.0,<5.0",
        "boto3>=1.26.0,<2.0.0",
        "Pillow==10.0.0,<11.0.0",
        "numpy>=1.22.0,<2.0.0",
        "lz4>=4.0.0,<5.0.0",
        "zstd>=1.5.0,<2.0.0",
        "s3path>=0.4.0,<1.0.0",
    ],
)
