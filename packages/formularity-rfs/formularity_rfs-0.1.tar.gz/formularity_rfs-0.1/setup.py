
from setuptools import setup, find_packages

setup(
    name="formularity_rfs",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "spacy",
        "pymorphy2",
        "numpy",
        "scikit-learn"
    ],
    package_data={
        '': ['*.txt'],
    },
    entry_points={
        'console_scripts': [
            'formularity_rfs = formularity.your_module:main',  
        ],
    },
    author="Valeria Sidnenko",
    author_email="valsidnenko@gmail.com",
    description="Пакет для оценки формульности фольклорных песен на русском языке",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/valsidnenko/formularity_rfs",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
