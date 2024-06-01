from setuptools import setup

setup(
    name = "puffb",
    keywords = ["pufferpanel"],
    description = "puffb is a small python module for interacting with a Pufferpanel daemon.",
    version = "1.0",
    author = "powermaker450",
    author_email = "contact@povario.com",
    url = "https://github.com/powermaker450/puffb",
    download_url = "https://github.com/powermaker450/puffb/archive/refs/tags/v1.0.tar.gz",
    install_requires = ["requests"],
    py_modules = ["puffb"],
    license = "MIT"
)
