import click
import pkg_resources
from pathlib import Path
import pandas as pd

from mappings.TrailsAnalysis import analyse

dataDirectory = pkg_resources.resource_filename(pkg_resources.Requirement.parse('mappings'), 'mappings/data')

def validate_pos_int(ctx, param, value):
    if value < 0:
        raise click.BadParameter("Should be a positive integer.")
    return value

# Start main. Uses if __name__.. to support runpy (python -m mappings)
@click.command()
@click.option('--nwalks', default=1000000, help='Number of walks; default = 1,000,000')
@click.option('--errorThreshold', default=1.0, help='Error threshold used to refine data used, default = 1.0, recommended range = 0 - 1.0, (1.0 = total error is not greater than signal, 0 = no removal of high error signals) ')
@click.option('--lowSignalCutOff', default=1000, help='Removal of low intensity signals, default = 1,000, recommended range = 500 - 1,500 for Kinexus antibody microarray datasets, can be move up or down depending on the desire output network size')
@click.option('--panNormaliser', default=True, help='Normalises signals by available Pan-specific antibody data provided. Default = Yes (normalise)')
@click.option('--edgeUsage', default=False, is_flag=True, help='Add edge usage numbers to output .csv, not required for Cytoscape rendering, default=False')
@click.option('--minimumTrailLength', default=3, callback=validate_pos_int, help='The minimum number of edges a walk is required to pass through to be counted as a trail, default = 3, range = 1+, reducing this will result in more complex outputs which are less focused on pathway identification')
@click.option('--connection_network_path', type=click.Path(exists=True, readable=True, resolve_path=True), default=Path(dataDirectory) / 'input' / 'NetworkComplete.csv', help='Network of known phosphorylation connections.')

@click.argument('array_data_path', type=click.Path(exists=True, readable=True, resolve_path=True))
@click.argument('output_path', type=click.Path(exists=False, writable=True, resolve_path=True))

def main(nwalks, array_data_path, output_path, connection_network_path, errorthreshold, lowsignalcutoff, pannormaliser, edgeusage, minimumtraillength):

	analyse(
		arrayData = pd.read_csv(array_data_path),
		connectionNetwork = pd.read_csv(connection_network_path),
		outputPath = output_path,
		nWalks = nwalks,
		errorThreshold = errorthreshold, 
		lowSignalCutOff = lowsignalcutoff,
		panNormaliser = pannormaliser,
		edgeUsage = edgeusage,
		minimumTrailLength= minimumtraillength
	)

if __name__ == '__main__':
	main()
	#Add no further lines