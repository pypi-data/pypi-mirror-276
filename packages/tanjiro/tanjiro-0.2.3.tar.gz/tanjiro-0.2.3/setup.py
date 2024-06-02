# setup.py

from setuptools import setup, find_packages

setup(
    name='tanjiro',
    version='0.2.3',  # Update this line
    packages=find_packages(),
    description='A simple library to interact with various APIs including ChatGPT, YouTube, Instagram, and more.',
    author='Vikas',
    author_email='vgboss91@gmail.com',
    url='https://github.com/tanjiro-851/tanjiro',  # Update with your actual URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests',
        'undetected-chromedriver',
        'selenium',
        'yt-dlp',  # Add yt-dlp to the list of dependencies
    ],
    python_requires='>=3.6',
)
