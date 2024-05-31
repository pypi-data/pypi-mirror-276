# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tramp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tramp',
    'version': '0.1.1',
    'description': 'No idea but we have a result type!',
    'long_description': 'No idea but we have a result type!\n',
    'author': 'Zech Zimmerman',
    'author_email': 'hi@zech.codes',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
