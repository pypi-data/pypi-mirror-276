from setuptools import setup, find_packages

setup(
    name="betterstar",
    version="1.0.0",
    author="Ole Meiforth",
    description="A better looking star marker for matplotlib plots.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/muederotter/betterstar',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["numpy", "matplotlib"],
)
