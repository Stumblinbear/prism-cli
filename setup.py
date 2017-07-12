from setuptools import setup, find_packages

setup(
    name='Prism CLI',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,

    python_requires='>=3.4',
    scripts=["bin/prism"],

    author='Stumblinbear',
    author_email='stumblinbear@gmail.com',
    description='',
    keywords='prism cli nginx apache gunicorn service',
    url='https://github.com/Stumblinbear/prism-cli'
)
