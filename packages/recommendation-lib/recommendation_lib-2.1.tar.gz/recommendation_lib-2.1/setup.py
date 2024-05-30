import setuptools


setuptools.setup(
    name="recommendation_lib",
    version="2.1",
    author="Giorgos Panagou",
    author_email="g.panagou94@gmail.com",
    description="Package containining recommendation algorithm",
    packages= setuptools.find_packages(include=['app', 'app.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    include_package_data=True,
    package_data={
        'app': ['data/*.csv'],
    },
)