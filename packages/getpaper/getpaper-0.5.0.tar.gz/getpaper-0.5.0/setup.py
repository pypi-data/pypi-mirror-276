from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.5.0'
DESCRIPTION = 'getpaper - papers download made easy!'
LONG_DESCRIPTION = 'A package with python functions for downloading papers'

# Setting up
setup(
    name="getpaper",
    version=VERSION,
    author="antonkulaga (Anton Kulaga)",
    author_email="<antonkulaga@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'pycomfort>=0.0.15',
        'click',
        'pynction',
        'langchain>=0.2.1',
        'langchain_community>=0.2.1',
        'scidownl>=1.0.2',
        'semanticscholar>=0.8.1',
        'Deprecated',
        'PyMuPDF>=1.24.4',
        "unpywall>=0.2.3",
        "nest_asyncio>=1.6.0",
        "chardet",
        "transformers"
    ],
    extras_require={
        'selenium': ['selenium', 'webdriver-manager'],
        'unstructured': [
            'pdfminer.six',
            'unstructured>=0.10.25',
            'unstructured-inference>=0.7.21',
            'unstructured[local-inference]',
            'unstructured.PaddleOCR>=2.6.1.3'
            #'git+https://github.com/facebookresearch/detectron2.git'
        ],
        'plumber': ['pdfplumber>=0.10.3']
    },
    keywords=['python', 'utils', 'files', 'papers', 'download'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
     "console_scripts": [
         "download=getpaper.download:app",
         "parse=getpaper.parse:app"
     ]
    }
)
