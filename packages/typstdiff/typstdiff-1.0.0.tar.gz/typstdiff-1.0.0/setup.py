# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typstdiff']

package_data = \
{'': ['*']}

install_requires = \
['jsondiff>=2.0.0,<3.0.0', 'pandoc>=2.3,<3.0', 'typst>=0.11.0,<0.12.0']

entry_points = \
{'console_scripts': ['typstdiff = main:main']}

setup_kwargs = {
    'name': 'typstdiff',
    'version': '1.0.0',
    'description': 'Tool made with Pandoc to compare two files with typst extension.',
    'long_description': '# TypstDiff\n### Dominika Ferfecka, Sara Fojt, Małgorzata Kozłowska\n\n## Introduction\nTool created with Pandoc to compare two typst files. It marks things\ndeleted from first file and marks differently things added to the second file.\n\n## Run documentation\nAll information about tool, its working process and how to use it is located\nin documentation written in mkdocs. To run documentation server use command\n`mkdocs serve` \nin the folder `documentation`.\nIf mkdocs is not installed use command `pip install mkdocs` or run virtual environment\n`poetry shell` and install all dependencies with `poetry install` (poetry can be installed\nwith `pip install poetry`)\n\n### Issues\nAs both tools - Pandoc and Typst are new and still developing there is no full support\nfor typst in Pandoc. Because of that it is not possible to notice all changes made\nin files, but tool will be developed.',
    'author': 'Sara Fojt',
    'author_email': '01169167@pw.edu.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
