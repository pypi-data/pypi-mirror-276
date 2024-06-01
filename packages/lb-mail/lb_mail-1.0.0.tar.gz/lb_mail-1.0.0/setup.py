import setuptools

setuptools.setup(
    name="lb-mail",
    version="1.0.0",
    author="Lucas Barros",
    author_email="lucasbarros2000@hotmail.com",
    description="Library with data models by lb services",
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
