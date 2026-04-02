from setuptools import setup, find_packages

setup(
    name="cell_search",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "dash",
        "matplotlib",
        "pandas==2.3.3; python_version < '3.11'",
        "pandas==3.0.1; python_version >= '3.11'",
        "pyperclip",
    ],

)