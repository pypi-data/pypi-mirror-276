from setuptools import setup, find_packages

setup(
    name='parameters_fooetall',
    version='0.1',
    license='MIT',
    author = 'Benny Antony',
    author_email = 'bennyantony2500@gmail.com',      
  url = 'https://github.com/bennyantony2500/parameters_fooetall',
  download_url = 'https://github.com/bennyantony2500/parameters_fooetall/archive/refs/tags/v.1.0.tar.gz',
    packages=find_packages(),
    install_requires=['argparse']
)