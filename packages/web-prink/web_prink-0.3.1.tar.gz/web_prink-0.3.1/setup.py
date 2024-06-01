# coding: utf-8

from setuptools import setup, find_packages
import os
import sys

# https://setuptools.pypa.io/en/latest/userguide/quickstart.html

# https://setuptools.pypa.io/en/latest/userguide/quickstart.html
# pip install --upgrade pip
# pip install --upgrade build
# pip install --upgrade setuptools
# python3 -m pip install --upgrade twine
# python3 -m build
# python3 -m twine upload --repository testpypi dist/*
# pip3 install --no-deps --index-url https://test.pypi.org/simple {package_name}

base_dir = os.path.dirname(__file__)
req_txt_path = os.path.join(base_dir, "requirements.txt")
ver_path = os.path.join(base_dir, "web_prink")
ver_path = os.path.join(ver_path, "__version__.py")

# with open(req_txt_path, "r", encoding="utf-8") as fd:
#     requires = fd.read().splitlines()  # thx, python12

main_ns = {}
with open(ver_path, "r", encoding="utf-8") as ver_file_fd:
    exec(ver_file_fd.read(), main_ns)

setup(
    name="web_prink",
    version=main_ns["__version__"],
    install_requires=["gradio", "pypdf"],
    packages=find_packages(
        # All keyword arguments below are optional:
        where='.',  # '.' by default
        include=['web_prink'],  # ['*'] by default
    ),
    entry_points={
        "console_scripts": [
                "web_prink = web_prink.main:main",
            ]
    },
    # include_package_data=True,  # setuptools is so stupid...
    # package_data={
    #     "static": ["static/execs.json"]
    # }
)
