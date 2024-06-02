from setuptools import setup

setup(
    name='bosk',
    version='0.0.1',
    description='Tree-based models in Python',
    author='João Bravo',
    url='https://github.com/ajoo/bosk',
    packages=['bosk'],
    package_dir={'': 'src'},
    install_requires=[
        'cffi>=1',
        'numpy',
        'scipy',
        'tqdm',
    ],
    setup_requires=['cffi>=1'],
)
