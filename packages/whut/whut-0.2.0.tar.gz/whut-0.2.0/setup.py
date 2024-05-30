from setuptools import setup, find_packages

# Function to read the requirements.txt file
def read_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='whut',
    version='0.2.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'whut=whut.cli:main',
        ],
    },
    install_requires=[
        'google-generativeai',
    ],
    author='Priyanshu K',
    twitter="https://twitter.com/pkdevaa",
    author_email='priyanshu.txt@gmail.com',
    description='A CLI tool to instantly search the internet using Google Generative AI in decluttered manner.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pkdeva/whut',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
