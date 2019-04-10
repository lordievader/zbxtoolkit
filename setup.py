from setuptools import setup

setup(
    name='zbxtoolkit',
    version='0.1',
    description='Functions for managing Zabbix via the API.',
    author='Olivier van der Toorn',
    author_email='oliviervdtoorn@gmail.com',
    packages=['zbxtoolkit'],
    install_requires=['pyzabbix', 'pyyaml', 'dnspython'],
)
