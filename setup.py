import setuptools
from sys import path

with open('requirements.txt') as f:
	requirements = f.readlines()

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
	name='ClevelandMuseumArt',
	version='0.1.0',
	author='Michael McIntyre',
	author_email='wtfender.cs@gmail.com',
	description='Python wrapper for Cleveland Museum of Art Open Access API',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/WTFender/CMA',
	packages=setuptools.find_packages(),
	install_requires=requirements,
	entry_points = {
		'console_scripts': ['cma=CMA.cli:main']
	},
	classifiers=[
		'Programming Language :: Python :: 3',
		'Operating System :: OS Independent'
	]
)
