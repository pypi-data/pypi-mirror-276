import setuptools

with open('requirements.txt', "r") as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygeoflow",
    version="0.0.1",
    description="A python package that helps you create geographic workflows within a cloud data warehouse. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mkeller3/pygeoflow",
    author="Michael Keller",
    author_email="michaelkeller03@gmail.com",
    license="MIT License",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=required,
    entry_points={
        "console_scripts": [
            "pygeoflow=pygeoflow.__main__:main",
        ]
    },
)