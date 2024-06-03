from setuptools import setup, find_packages

setup(
    name='cs_ob_mini_scikit_learn',
    version='0.1.8',
    author='basma-arnaoui',
    author_email='basma.arnaoui@um6p.ma',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'scikit-learn', 
        'clone',
        'pandas',
         
    ],
    python_requires='>=3.6',
    description='A minimal implementation of scikit-learn like functionalities',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Basma-Arnaoui/Mini-Scikit-Learn/tree/main',
)
