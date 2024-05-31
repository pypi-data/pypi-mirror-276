# setup.py

from setuptools import setup, find_packages

setup(
    name='tanjiro',
    version='0.2.0',
    packages=find_packages(),
    description='A simple library to interact with a ChatGPT API',
    author='vikas ',
    author_email='vgboss91@gmail.com',
    url='https://github.com/tanjiro-851/tanjiro',  # Update with your actual URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
