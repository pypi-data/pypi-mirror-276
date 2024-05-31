from setuptools import setup, find_packages

setup(
    name="hashtag_utils",
    version="0.5.6",
    packages=["hashtag_utils"],
    author="Aditya Patange",
    author_email="contact.adityapatange@gmail.com",
    description="Simple LLM-powered hashtag utilities.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://github.com/AdiPat/hashtag_utils",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        "openai",
        "python-dotenv",
    ],
)
