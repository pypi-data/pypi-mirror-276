from setuptools import setup, find_packages

setup(
    name='cropimg',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'pillow',
        'adb-tool-py>=0.1.2',
    ],
    entry_points={
        'console_scripts': [
            'cropimg=cropimg.cropimg:main',
        ],
    },
    author='Shota Iuchi',
    author_email='shotaiuchi.develop@gmail.com',
    description='Cropping images',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords='crop, image, adb, screenshot',
    url='https://github.com/ShotaIuchi/crop-image',
)