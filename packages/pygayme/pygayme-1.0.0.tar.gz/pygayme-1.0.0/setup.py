from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pygayme",
    version="1.0.0",
    author="mr.r",
    description="pygayme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/your-username/your-repo",
    packages=["pygayme"],
    install_requires=["pygame-ce"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)