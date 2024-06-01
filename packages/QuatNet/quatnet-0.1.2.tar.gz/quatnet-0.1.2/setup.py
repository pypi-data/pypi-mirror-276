# setup.py
from setuptools import setup, find_packages

setup(
    name='QuatNet',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'torch==2.3.0',
        'numpy==1.24.4',
        'scipy==1.10.1'
    ],
    author='aryan chaudhary',
    author_email='datasenseiaryan@gmail.com',
    description='A PyTorch-based library for quaternion neural networks',
    long_description=open('README.MD').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DataSenseiAryan/QuatNet',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='==3.8.19',
)
