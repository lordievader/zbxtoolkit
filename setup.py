from setuptools import setup

setup(
    name='zbxtoolkit',
<<<<<<< HEAD
    version='0.2.1',
||||||| parent of e310438... Add broken_lld function
    version='0.1.1',
=======
    version='0.2.0',
>>>>>>> e310438... Add broken_lld function
    description='Functions for managing Zabbix via the API.',
    author='Olivier van der Toorn',
    author_email='oliviervdtoorn@gmail.com',
    packages=['zbxtoolkit'],
    install_requires=['pyzabbix', 'pyyaml', 'dnspython'],
)
