from setuptools import setup


def get_version():
    version = {}
    with open("chgksuite_tk/version.py", encoding="utf8") as f:
        exec(f.read(), version)
    return version["__version__"]

long_description = """**chgksuite-tk** is a GUI wrapper around https://gitlab.com/peczony/chgksuite"""


setup(
    name="chgksuite_tk",
    version=get_version(),
    author="Alexander Pecheny",
    author_email="ap@pecheny.me",
    description="A GUI wrapper for chgksuite using tkinter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/peczony/chgksuite_tk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["chgksuite_tk"],
    entry_points={"console_scripts": ["chgkt = chgksuite_tk.__main__:main"]},
    install_requires=[
        "chgksuite"
    ]
)
