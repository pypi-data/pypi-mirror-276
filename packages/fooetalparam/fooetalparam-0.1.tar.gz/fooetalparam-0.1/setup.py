from setuptools import setup, find_packages

setup(
    name='fooetalparam',
    version='0.1',
    license='MIT',
    author = 'Benny Antony',
    author_email = 'bennyantony2500@gmail.com',      
  url = 'https://github.com/bennyantony2500/fooetalparam',
  download_url = 'https://github.com/bennyantony2500/fooetalparam/archive/refs/tags/v_1.tar.gz',
    packages=find_packages(),
    install_requires=['pytest','argparse']
)