# coding=utf-8
from setuptools import setup, find_packages

setup(
    name='wechat',  # package name
    version='0.1',  # package version
    author='',
    author_email='',
    description='',
    keywords=['src'],
    package=find_packages(include=['src']),
    include_package_data=True,
    platforms="wechat",
    entry_points={
        'console_scripts': [
            'run=run:main'
        ]
    },
    zip_safe=False
)
