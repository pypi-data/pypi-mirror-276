# -*- coding: utf-8 -*-

print("__file__: " + __file__)


with open("README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()
    # print("LONG_DESCRIPTION: " + LONG_DESCRIPTION)
    f.close()


PACKAGE_DIR = 'src'


import os 
print("cwd: " + os.getcwd())

INSTALL_REQUIRES = []
try:
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        for line in f.read().splitlines():
            INSTALL_REQUIRES.append(line.strip())
        print("INSTALL_REQUIRES: ", INSTALL_REQUIRES)
        f.close()
except Exception as e:
    print("FILE I/O ERROR: ", e)
        


import setuptools


setuptools.setup(
    name="dselib",
    version="0.1.3",
    author="innovata",
    author_email="iinnovata@gmail.com",
    description="NETVIBES / Data Science Experience",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=f"https://github.com/innovata/DataScienceExperience",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": PACKAGE_DIR},
    packages=setuptools.find_packages(PACKAGE_DIR),
    python_requires=">=3.8",
    install_requires=INSTALL_REQUIRES,
)
