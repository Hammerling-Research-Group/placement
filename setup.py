"""
Setup configuration for the placement package.
"""

from setuptools import setup, find_packages

setup(
    name='placement',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['numpy', 'setuptools'],
    author='Meng Jia, Troy Sorensen, Philip Waggoner, Dorit Hammerling',
    author_email='mjia@mines.edu, trsorensen@mines.edu, philip.waggoner@mines.edu, hammerling@mines.edu',
    maintainer='Meng Jia',
    maintainer_email='mjia@mines.edu',
    description='A Python package for optimizing continuous monitoring sensor placement on oil and gas sites',
    long_description=(
        open('README.md', encoding='utf-8').read()
    ),
    long_description_content_type='text/markdown',
    url='https://github.com/Hammerling-Research-Group/placement',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
