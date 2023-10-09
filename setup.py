from setuptools import setup, find_packages

setup(
    name='grps',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click==8.1.7',
        'ftfy==6.1.1',
        'grpcio==1.59.0',
        'grpcio-tools==1.59.0',
        'joblib==1.3.2',
        'langcodes==3.3.0',
        'msgpack==1.0.7',
        'nltk==3.8.1',
        'protobuf==4.24.4',
        'PyPDF2==3.0.1',
        'regex==2023.10.3',
        'stemming==1.0.1',
        'tqdm==4.66.1',
        'wcwidth==0.2.8',
        'wordfreq==3.0.3',
    ],
    entry_points={
        'console_scripts': [
            'grpstart = src.server:serve'
        ]
    }
)