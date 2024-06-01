from setuptools import setup

setup(
    name='simkit',
    version='0.0.0',
    description='SimKit: A Simulation Toolkit For Computer Animation',
    url='https://github.com/otmanon/pal',
    author='Otman Benchekroun',
    author_email='otman.benchekroun@mail.utoronto.ca',
    license='MIT',
    packages=['simkit'],
    install_requires=['scipy',
                      'numpy',
                      'polyscope',
                      'libigl'
                      ],

    classifiers=[
    ],
)