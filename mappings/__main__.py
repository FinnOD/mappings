import click
import pkg_resources
from pathlib import Path
import pandas as pd

from mappings.TrailsAnalysis import analyse

dataDirectory = pkg_resources.resource_filename(pkg_resources.Requirement.parse('mappings'), 'mappings/data')

# Start main. Uses if __name__.. to support runpy (python -m mappings)
@click.command()
@click.option('--nwalks', default=1000000, help='Number of walks.')
@click.option('--connection_network_path', type=click.Path(exists=True, readable=True, resolve_path=True), default=Path(dataDirectory) / 'input' / 'NetworkComplete.csv', help='Network of known phosphorylation connections.')
@click.argument('array_data_path', type=click.Path(exists=True, readable=True, resolve_path=True))
@click.argument('output_path', type=click.Path(exists=False, writable=True, resolve_path=True))
def main(nwalks, array_data_path, output_path, connection_network_path):

	analyse(
		arrayData = pd.read_csv(array_data_path),
		connectionNetwork = pd.read_csv(connection_network_path),
		outputPath = output_path,
		nWalks = nwalks
	)
	# cli()

if __name__ == '__main__':
	main()
	#Add no further lines