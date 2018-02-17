from setuptools import setup, find_packages

setup(
    name='crud-api-with-tavern-tests',
    version='0.0.1',
    description=('This is a project for practicing creating a CRUD API in ',
                 'Falcon and testing it with tavern.'),
    url='https://github.com/alysivji/crud-api-with-tavern-tests',
    author='Aly Sivji',
    author_email='alysivji@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['tests', ]),
    install_requires=[''],
    download_url='https://github.com/alysivji/crud-api-with-tavern-tests',
)
