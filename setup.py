
from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
	name='mappings',
	version='0.1.0',
	description="Mapping and Analysis of Phosphorylation Pathways Identified through Network/Graph Signalling",
	long_description=long_description,
	long_description_content_type='text/markdown',
	author="Finn O'Donoghue",
	author_email='finnodonoghue@gmail.com',
	url='https://github.com/finnod/mappings',
	
	keywords=[
		'mapping',
		'analysis',
		'phosphorylation',
		'pathways',
		'network',
		'graph',
		'signalling',
		'kinase',
		'kinases',
		'kinexus',
		'protein',
		'informatics',
		'bioinformatics',
	],
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Topic :: Scientific/Engineering :: Bio-Informatics',
		'Topic :: Scientific/Engineering :: Information Analysis',
		'Topic :: Scientific/Engineering :: Mathematics',
		'Intended Audience :: End Users/Desktop',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: POSIX',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3'
	],

	packages=['mappings'],
	entry_points={
		'console_scripts': [
			'mappings=mappings.__main__:main',
		],
	},
	package_data={'mappings': [
		'*.csv',
		'data/input/*',
		'data/*'
		'.xml'
		'images/*'
		'.jpg',
		'.png'
		]
	},

	install_requires=[
		'numpy',
		'pandas',
		'click',
		'pathlib',
		'networkx',
		'tqdm'
	],
)
