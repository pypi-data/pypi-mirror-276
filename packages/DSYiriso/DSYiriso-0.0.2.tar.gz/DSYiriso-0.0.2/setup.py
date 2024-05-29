import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()


setuptools.setup(
    name="DSYiriso",
    version="0.0.2",
    author="yichi zhang",
    author_email="kszyc1001@163.com",
    description="Data structure in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Yirios/Data-Structure", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8'
)

#   python setup.py sdist build
#   twine upload dist/*  

#   git tag [new version] -m "detail"
#   git push origin [new version]