import os
from setuptools import setup

MONITOR_PACKAGE = 'hajau'
CLI_PACKAGE = 'cli'

VERSION = '0.0.1'
LONG_DESCRIPTION = 'Simple monitor'

setup(
    name=MONITOR_PACKAGE,
    packages=[MONITOR_PACKAGE, CLI_PACKAGE],
    install_requires=[
        'httplib2',
        'pyrebase'
    ],
    entry_points={
        'console_scripts': [
            'dlm = cli.login:main',
            ]
    },
    package_data={'': [VERSION, LONG_DESCRIPTION]},
    version=VERSION,
    description=LONG_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='HaJaU',
    author_email='ahihi@notexist.com',
    url='https://hajaulee.github.io/dl/',
)