from setuptools import setup

setup(name='wirelesstraitor',
      version='0.3',
      description='Little tool to grab geolocations from probe requests',
      url='https://github.com/dmaendlen/wireless-traitor',
      author='David Mändlen',
      author_email='1_wirelesstraitor@bifroe.st',
      license='Apache 2.0',
      packages=['wirelesstraitor'],
      install_requires = [
        'scapy-python3',
        'requests',
        'simplejson',
        'multiprocess',
      ],
      scripts = [
        'bin/wirelesstraitor-mock',
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      )
