from setuptools import setup, find_packages
# see https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/
setup(
    name='pygeoapicustom',
    version='0.1.0',
#    packages=['extendedproviders'],
    packages=find_packages(),
    install_requires=['mpi4py>=2.0',
                      'numpy',
                      ],

    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
    ],
)
