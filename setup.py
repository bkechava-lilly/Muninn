"""Setup script for installing hugs."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'muninn',
    'author': 'Bobak D Kechavarzi',
    'url': 'Project URL https://github.com/bkechava-lilly/Muninn',
    'download_url': 'https://github.com/bkechava-lilly/Muninn',
    'author_email': 'kechavarzi_bobak_d@lilly.com',
    'version': '0.1',
    'install_requires': ['numpy', 'matplotlib', 'whoosh', 'dash',
                         'dash-core-components', 'dash-renderer',
                         'dash_table_experiments', 'pandas', 'markdown'],
    'packages': ['muninn', 'muninn.display', 'muninn.document_management'],
    'scripts': [],
    'name': 'muninn'
}

setup(**config)
