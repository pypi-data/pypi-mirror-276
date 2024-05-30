from setuptools import setup, find_packages

setup(
    name='sentiment_analysis_model',
    version='0.0.6',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'pydantic',
        'strictyaml',
        'joblib',
        'nltk'
    ],
)
