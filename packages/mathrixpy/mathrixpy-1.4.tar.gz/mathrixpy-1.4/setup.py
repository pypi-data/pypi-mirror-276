from setuptools import setup, find_packages

setup(
    name="mathrixpy",
    version="1.4",
    author="AmJoJADeOrg",
    license='MIT',
    author_email="glroberto1810@gmail.com",
    description="mathrixpy es una biblioteca de Python para realizar operaciones matriciales. Permite la creación, manipulación y operaciones aritméticas con matrices. Esta biblioteca es útil para aplicaciones matemáticas y científicas que requieren cálculos matriciales.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Ampere-G/mathrixPy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)