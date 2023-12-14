from setuptools import setup, find_packages

setup(
    name='zenithfit', 
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'fastapi[all]','pre-commit','pytest'
    ],

    author='Tim Krebs',
    author_email='timkrebs9@gmail.com',
    description='Eine kurze Beschreibung Ihres Projekts',
    license='MIT',
    keywords='FastAPI, API, REST, Python',
    url=''
)
