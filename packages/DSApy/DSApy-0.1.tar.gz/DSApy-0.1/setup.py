from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="DSApy",
    version="0.1",
    author="Soumya Chakraborty",
    author_email="soumyachakraborty198181@gmail.com",
    description="This helps in using of different data structure and algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Use 'text/x-rst' if your README is in reStructuredText
    url="https://github.com/Soumya-Chakraborty/DSApy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
