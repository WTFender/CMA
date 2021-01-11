import setuptools

with open('requirements.txt') as f:
	requirements = f.readlines()

setuptools.setup(
	name='CMA',
	version='0.1',
	author='Michael McIntyre',
	author_email='wtfender.cs@gmail.com',
	description='Python API Wrapper for Cleveland Museum of Art Open Access API',
	long_description='Python API Wrapper for Cleveland Museum of Art Open Access API',
	long_description_content_type='text/plain',
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
