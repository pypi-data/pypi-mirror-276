from setuptools import setup, find_packages

setup(
    name='UnionCalLib',
    version='0.122',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'run=UnionCalLib.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
