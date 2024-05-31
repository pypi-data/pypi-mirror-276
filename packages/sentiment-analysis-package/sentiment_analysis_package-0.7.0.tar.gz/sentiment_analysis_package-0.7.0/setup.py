from setuptools import setup, find_packages

setup(
    name='sentiment_analysis_package',
    version='0.7.0',
    packages=find_packages(),
    include_package_data=True,
    package_data= {
       'sentiment_model' : ['config.yml'],
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
