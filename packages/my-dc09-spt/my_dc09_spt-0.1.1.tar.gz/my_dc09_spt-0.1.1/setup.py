import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my_dc09_spt",
    author="Jacq. van Ovost",
    author_email="jacq.van.ovost@gmail.com",
    description="A dialler implementation using the SIA-DC09 protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['DC09', 'SIA DC09', 'SPT', 'Alarm transmitter'],
    url="https://github.com/jvanovost/dc09_spt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['cryptography>=3.1'],
    setuptools_git_versioning={
        "enabled": True,
        "starting_version": "0.1.1",
    },
    setup_requires=["setuptools-git-versioning>=2.0,<3"]
)

