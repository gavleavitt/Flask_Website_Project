from setuptools import setup
# see https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/
setup(
    name='flaskcustomutil',
    version='0.1.0',
    packages=['PyGeoApiExtended','Boto3AWS','ErrorEmail','flaskAuth'],
    install_requires=[],
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
    ],
)
