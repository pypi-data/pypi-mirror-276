from setuptools import setup, find_packages

setup(
    name='sentiment_analysis_package',
    version='0.8.0',
    packages=find_packages(),
    include_package_data=True,
    package_data= {
       'sentiment_model' : ['config.yml', '*.pkl', 'datasets/twitter_training.csv'],
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
