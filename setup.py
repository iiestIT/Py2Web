from setuptools import setup, find_packages


setup(
    name='PyWeb',
    version='0.0.1.dev1',
    description='A package to perform requests to any website and render there js based on pyside2',
    url='https://github.com/iiestIT/PyWeb',
    author='iiestIT',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP :: Browsers"
    ],
    keywords='pyside2 browser engine rendering',
    python_requires='3.9',
    packages=find_packages()
)
