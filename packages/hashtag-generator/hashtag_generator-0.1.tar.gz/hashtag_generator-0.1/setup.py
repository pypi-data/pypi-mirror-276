from setuptools import setup, find_packages

setup(
    name="hashtag-generator",
    version="0.1",
    packages=find_packages(),
    author="Aditya Patange",
    author_email="contact.adityapatange@gmail.com",
    description="An LLM-powered hashtag generator written in Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://github.com/AdiPat/hashtag-generator",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)
