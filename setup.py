from setuptools import setup, find_packages

setup(
    name="geojsonfile_image_attacher",
    version="0.2.0",
    author="Subekshya Subedi",
    author_email="subekshyasubedi26@gmail.com",
    description="Python package to automatically attach images to GeoJSON features",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/subekshya-s/geojson_image_attacher.git",
    packages=find_packages(),
    install_requires=[
        "rapidfuzz>=3.0.0",        
    ],
    entry_points={
        "console_scripts": [
            "geojson-attach=geojsonfileandimageattacher.cli:main",  
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

