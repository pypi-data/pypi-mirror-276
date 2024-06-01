import setuptools

VERSION = "0.6.2"

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(name='termite_toolkit',
                 version=VERSION,
                 description='scibite-toolkit - python library for calling TERMite, TExpress and other tools, and processing results',
                 url='https://github.com/elsevier-health/scibite-toolkit',
                 install_requires=[
                     "beautifulsoup4>=4.12.3",
                     "bs4==0.0.2",
                     "certifi>=2024.2.2",
                     "charset-normalizer>=3.3.2",
                     "click>=8.1.7",
                     "idna>=3.7",
                     "joblib>=1.4.2",
                     "nltk>=3.8.1",
                     "numpy>=1.24",
                     "pandas>=2",
                     "python-dateutil>=2.9.0.post0",
                     "pytz>=2024.1",
                     "regex>=2024.5.15",
                     "requests>=2.32.2",
                     "six>=1.16.0",
                     "tqdm>=4.66.4",
                     "tzdata>=2024.1",
                     "urllib3>=2.2.1"
                 ],
                 extras_require={'test': ['filelock','pytest']},
                 author='SciBite',
                 author_email='help@scibite.com',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 license='Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License',
                 packages=setuptools.find_packages(),
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "Operating System :: OS Independent",
                 ],
                 data_files=[("", ["LICENSE.txt"])],
                 zip_safe=False)
