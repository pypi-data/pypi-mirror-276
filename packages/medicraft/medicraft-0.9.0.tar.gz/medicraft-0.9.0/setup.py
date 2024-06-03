# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['medicraft',
 'medicraft.datasets',
 'medicraft.experiments',
 'medicraft.models',
 'medicraft.pipeline',
 'medicraft.pipeline.blocks',
 'medicraft.trackers',
 'medicraft.trainers',
 'medicraft.utils',
 'medicraft.validation']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==6.0.1',
 'denoising-diffusion-pytorch==1.9.4',
 'ema-pytorch==0.3.1',
 'lightning==2.2.1',
 'matplotlib==3.8.4',
 'pandas==2.2.2',
 'pillow==10.3.0',
 'pydantic==2.7.2',
 'scikit-learn==1.4.2',
 'seaborn==0.13.2',
 'torch==2.3.0',
 'torchmetrics==1.3.1',
 'torchvision==0.18.0',
 'tqdm==4.66.2',
 'umap-learn==0.5.5',
 'wandb==0.16.3']

setup_kwargs = {
    'name': 'medicraft',
    'version': '0.9.0',
    'description': 'Medicraft synthetic dataset generator',
    'long_description': None,
    'author': 'Filip Patyk',
    'author_email': 'fp.patyk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
