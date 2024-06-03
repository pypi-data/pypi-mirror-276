from setuptools import find_packages, setup

setup(
    name='m-o-mini-scikit-learn-ai-project', 
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        # Add any other dependencies here
    ],
    author='Maha,Oumaima',
    author_email='maha.hanif@um6p.ma',
    description='A mini implementation of scikit-learn with various machine learning models and utilities.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mahatun/Mini-Scikit-Learn.git',
    
)
