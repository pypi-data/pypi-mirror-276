from setuptools import setup, find_packages

setup(
    name='parameter_fooetal',
    version='0.1',
    license='MIT',
    author = 'Benny Antony',
    author_email = 'bennyantony2500@gmail.com',      
  url = 'https://github.com/bennyantony2500/parameter_fooetal',
  download_url = 'https://github.com/bennyantony2500/parameter_fooetal/archive/refs/tags/v_01.tar.gz',
    packages=find_packages(),
    install_requires=['pytest','argparse']
)