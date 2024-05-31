# setup.py

from setuptools import setup, find_packages

setup(
    name='ndpi_demerger',
    version='0.1.2',
    description='A package for extracting patches from NDPI images',
    author='Thirteen',
    author_email='506607814@qq.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'openslide-python',
        'Pillow',
        'numpy',
        'scikit-image'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)


