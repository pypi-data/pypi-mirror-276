# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_object_acl', 'django_object_acl.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=5.0.6,<6.0.0']

setup_kwargs = {
    'name': 'django-object-acl',
    'version': '0.1.0',
    'description': 'Adds object level permission for your models',
    'long_description': None,
    'author': 'Noam Ben-Yechiel',
    'author_email': 'nbenyechiel@twistbioscience.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
