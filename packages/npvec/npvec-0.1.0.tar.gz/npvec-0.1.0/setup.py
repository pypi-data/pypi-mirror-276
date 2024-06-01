from setuptools import find_packages, setup

setup(
    name='npvec',
    version=open('version.txt').read().strip(),
    author='Evan Raw',
    author_email='evanraw.ca@gmail.com',
    description='Numpy ndarray wrapper with swizzling',
    license='MIT',
    install_requires=[],
    packages=find_packages()
)
