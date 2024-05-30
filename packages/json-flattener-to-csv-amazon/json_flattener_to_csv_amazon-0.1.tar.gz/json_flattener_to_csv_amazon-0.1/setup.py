# setup.py
from setuptools import setup, find_packages

setup(
    name='json-flattener-to-csv-amazon',  # Updated package name
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas'
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A package to flatten JSON data and convert it to CSV for Amazon',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/json-flattener-to-csv-amazon',  # Update with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
