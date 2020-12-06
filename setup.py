from setuptools import setup, find_packages


setup(
    name='PyWeb',
    version='0.0.1.dev1',
    description='A python package to perform HTTP requests to websites and render their content.',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/iiestIT/PyWeb',
    author='iiestIT',
    author_email='it.iiest.de@gmail.com',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "License :: OSI Approved :: MIT License"
    ],
    keywords='pyside2 browser engine rendering',
    python_requires='>=3.8',
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines()
)
