from setuptools import setup, find_packages

setup(
    name="pdlogger",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="Maruthi Varaprasad",
    author_email="your.email@example.com",
    description="An example package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/example_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
