from setuptools import setup


def get_version():
    version = {}
    with open("chgksuite_qt/version.py", encoding="utf8") as f:
        exec(f.read(), version)
    return version["__version__"]

long_description = """**chgksuite-qt** is a GUI wrapper around https://gitlab.com/peczony/chgksuite"""


setup(
    name="chgksuite_qt",
    version=get_version(),
    author="Alexander Pecheny",
    author_email="ap@pecheny.me",
    description="A GUI wrapper for chgksuite using PyQt6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/peczony/chgksuite_qt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["chgksuite_qt"],
    entry_points={"console_scripts": ["chgkq = chgksuite_qt.__main__:main"]},
    install_requires=[
        "chgksuite",
        "PyQt6"
    ]
)
