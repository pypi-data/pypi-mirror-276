from setuptools import setup, find_packages

setup(
    name='Maslib',
    version='0.2.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'phik',
        'matplotlib',
        'scikit-learn',
        'catboost',
        'joblib',
        'wordcloud',
        'xgboost',
        'nltk',
        'pyodbc',
        'mysql-connector-python',
        'pymongo',
        'psycopg2-binary',
        'PyYAML',
        'fastavro',
        'pyorc',
        'pdfplumber',
        'pyreadstat',
        'cbor2',
        'sqlalchemy',
        'sas7bdat',
        'spacy'

    ],
    author='Alecsandr_C.V.V',
    author_email='dxomko@gmail.com',
    description='This is a library for optimizing code for python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
