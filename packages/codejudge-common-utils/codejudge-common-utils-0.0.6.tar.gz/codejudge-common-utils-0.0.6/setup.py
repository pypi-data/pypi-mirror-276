from setuptools import setup, find_packages


setup(
    name="codejudge-common-utils",
    version="0.0.6",
    description="A codejudge common util library for python to perform certain tasks.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Yash Mittal",
    author_email="akhil@codejudge.io",
    classifiers=
    [
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],

    packages=find_packages()
)
