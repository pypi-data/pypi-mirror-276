from setuptools import setup, find_packages

setup(
    name="mailbit",
    version="0.1.0",
    description="A simple library to send emails using the Mailbit API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Marcos",
    author_email="marcos.santos.filho.fl@gmail.com",
    url="https://github.com/marcossantosfl/mailbit-library-python",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*",
)
