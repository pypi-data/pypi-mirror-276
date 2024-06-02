import setuptools

setuptools.setup(
    name="lb-authorization",
    version="1.0.0",
    author="Lucas Barros",
    author_email="lucasbarros2000@hotmail.com",
    description="Library for control tokens service",
    packages=setuptools.find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)
