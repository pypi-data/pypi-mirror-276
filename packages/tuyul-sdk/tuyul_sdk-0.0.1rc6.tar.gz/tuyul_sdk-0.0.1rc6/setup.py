# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tuyul_sdk', 'tuyul_sdk._certificate']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.1,<3.0.0',
 'chardet>=5.2.0,<6.0.0',
 'colorama>=0.4.6,<0.5.0',
 'httpx[http2,socks]==0.27.0',
 'pycryptodomex>=3.20.0,<4.0.0',
 'random-user-agent>=1.0.1,<2.0.0',
 'requests==2.31.0',
 'sqlalchemy-utils>=0.41.2,<0.42.0',
 'sqlalchemy>=2.0.30,<3.0.0']

setup_kwargs = {
    'name': 'tuyul-sdk',
    'version': '0.0.1rc6',
    'description': '',
    'long_description': '',
    'author': 'Antoni Oktha Fernandes',
    'author_email': '37358597+DesKaOne@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
