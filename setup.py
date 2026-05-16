from setuptools import setup, find_packages
 

setup(

    name="geojsonfile_image_attacher",

    version="0.1.0",

    author="Subekshya Subedi",

    author_email="subekshyasubedi26@gmail.com",

    description="Python package to automatically  attach the images to the geojson file ",

    long_description=open("README.md", encoding="utf-8").read(),

    long_description_content_type="text/markdown",

    url="https://github.com/subekshya-s/geojson_image_attacher.git",

    packages=find_packages(),

    classifiers=[

        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

    ],

    python_requires='>=3.6',

)