# setup.py

from setuptools import setup, find_packages

setup(
    name='emu_data_loader',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'mne',
    ],
    author='Amir Hossein Daraie',
    author_email='adaraie1@jh.edi',
    description='A library to import EMU data from different centers into Python along with dynamical network model properties and other features',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/amirhdre/emu_data_loader',  # Replace with your actual URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)