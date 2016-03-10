try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
    'description': 'A very simple static site generator.',
    'author': 'Tyler Staples',
    'url': '',
    'download_url': '',
    'author_email': '',
    'version': '0.1',
    'install_requires': ['unittest'],
    'packages': ['SimpleSiteGen'],
    'scripts': [],
    'name': 'SimpleSiteGen'
}

setup(**config)