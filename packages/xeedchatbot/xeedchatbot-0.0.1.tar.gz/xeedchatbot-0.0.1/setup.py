import os
from setuptools import setup, find_packages

#taken from pip/setup.py
def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

setup(
    name = 'xeedchat',
    version=get_version(r"src\xeedchatbot\__init__.py"),
    packages = find_packages(
        where='src',
        include=['xeedchatbot.*']),
    package_dir={"": "src"},
    include_package_data=True,
    author='Neil Ortaliz',
    author_email='neillaurenceortaliz@gmail.com',
    description='Xeed ChatBot initializer for Frappe Bench',
    install_requires=[
    "langchain",
    "langchain_experimental",
    "langchain_openai",
    "pandas",
    "tabulate"
    ]
)