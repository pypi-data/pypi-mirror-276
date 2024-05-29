from setuptools import setup, find_packages

setup(
    name='recommendation_lib',
    version='1.0',
    author='Giorgos Panagou',
    author_email='g.panagou94@gmail.com',
    description='A recommendation engine library',
    packages=find_packages(),
    install_requires=[
        'requests',
        'numpy',
    ],
)