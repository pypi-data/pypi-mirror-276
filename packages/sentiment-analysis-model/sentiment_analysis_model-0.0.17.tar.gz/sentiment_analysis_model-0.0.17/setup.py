from setuptools import setup, find_packages

setup(
    name='sentiment_analysis_model',
    version='0.0.17',
    packages=find_packages(),
    include_package_data=True,
    package_data= {
       '' : ['config.yml'],
    },
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
