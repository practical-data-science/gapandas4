from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gapandas4',
    packages=['gapandas4'],
    version='0.003',
    license='MIT',
    description='GAPandas4 is a Python package for accessing the Google Analytics Data API for GA4 using Pandas',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Matt Clarke',
    author_email='matt@practicaldatascience.co.uk',
    url='https://github.com/practicaldatascience/gapandas4',
    download_url='https://github.com/practicaldatascience/gapandas4/archive/master.zip',
    keywords=['python', 'google analytics', 'ga', 'pandas', 'universal analytics', 'gapandas', 'ga4'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['pandas', 'google-analytics-data']
)
