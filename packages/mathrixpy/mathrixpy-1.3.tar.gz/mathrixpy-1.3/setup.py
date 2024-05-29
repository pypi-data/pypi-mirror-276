from setuptools import setup, find_packages

setup(
    name="mathrixpy",
    version="1.3",
    author="AmJoJADeOrg",
    license='MIT',
    author_email="glroberto1810@gmail.com",
    description="Operaciones con matrices",
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