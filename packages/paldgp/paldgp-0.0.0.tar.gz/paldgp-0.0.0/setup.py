from setuptools import setup

setup(
    name='paldgp',
    version='0.0.0',
    description='PAL: the Physics Animation Library',
    url='https://github.com/otmanon/pal',
    author='Otman Benchekroun',
    author_email='otman.benchekroun@mail.utoronto.ca',
    license='MIT',
    packages=['pal'],
    install_requires=['scipy',
                      'numpy',
                      'polyscope',
                      'libigl'
                      ],

    classifiers=[
    ],
)