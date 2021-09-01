from mappings.RandomTrail import *
from mappings.DatasetOrganisationNormalise import *
from mappings.DatasetOrganisation import *
from mappings.Merger import *
from mappings.NetworkasDiGraph import *
from itertools import chain
import pandas as pd
from pathlib import Path

pd.options.mode.chained_assignment = None  # default='warn'

########################################################################################################################
# Analysis criteria to set according to requirements

# ErrorThreshold = 1  # Lower = more stringent (0.01 - 10 (above 1 not recommended, 1 = 1:1 total error to change)
# LowSignalCutOff = 1000  # Change to desired value, older arrays 1000 recommended, newer 750 recommended
# PanNormaliser = False  # Do you want the phospho signals normalised by pan-signals?
########################################################################################################################

# splits trails into individual edges
def edgetally(datalist, SpecificNetwork):
	
	# splits trails list into edge list
	AllTrailEdgeUse = pd.DataFrame(chain.from_iterable(zip(x, x[1:]) for x in datalist))

	# Tally up edge usage and call all associated information to edges
	AllTrailEdgeUse.columns = ['Kinase', 'Substrate']
	TrailEdgeSummaryTable = pd.pivot_table(AllTrailEdgeUse, index=['Kinase', 'Substrate'], aggfunc='size')
	TrailEdgeSummary = pd.DataFrame(TrailEdgeSummaryTable).reset_index()
	TrailEdgeSummary.rename(inplace=True, columns={TrailEdgeSummary.columns[2]: 'TotalWalks'})
	TrailEdges = pd.merge(SpecificNetwork, TrailEdgeSummary, on=['Kinase', 'Substrate'])

	return TrailEdges

def analyse(
	arrayData: pd.DataFrame, 
	connectionNetwork: pd.DataFrame,
	outputPath: Path,
	nWalks: int = 1000,
	errorThreshold: float = 1.0, 
	lowSignalCutOff: float = 1000.0,
	panNormaliser: bool = True,
	edgeUsage: bool = False,
	minimumTrailLength: int = 3
	) -> None:

	# Caveats for dataset
	# Cross-reactive Signals need to be removed.
	# Biological replicate data needs to be averaged for the Signal data.

	########################################################################################################################
	# Dataset input
	# Format is the following columns; Uniport ID(1), Protein name(2), Phosphosite(3), Control Signal(4),
	# Control Signal Error(5), Test Signal (6), Test Signal Error (7)
	# ArrayData = pd.read_csv(r'Input/PfTrophData.csv')

	########################################################################################################################
	# ConnectionNetwork = pd.read_csv(r'Input\NetworkComplete.csv')  # import CompleteNetwork

	# Organisation of Dataset and determination of quartiles of the data
	if panNormaliser == True:
		PosDataCorrected, NegDataCorrected = DatasetOrganisationNormalise(arrayData, lowSignalCutOff, errorThreshold)
	else:
		PosDataCorrected, NegDataCorrected = DatasetOrganisation(arrayData, lowSignalCutOff, errorThreshold)

	# Merging of Network with Array dataset
	# Returns mapped dataset, Positive Network and Negative Network
	PosNetwork, NegNetwork = Merger(connectionNetwork, PosDataCorrected, NegDataCorrected)

	# Network as DiGraph and final edgelists
	PosEdges, NegEdges, PosNetworkFinal, NegNetworkFinal = NetworkasDiGraph(PosNetwork, NegNetwork)
	# PosNetwork.to_csv(r'Output/troph pos net.csv') #TODO Why? Re-implement - Can be deleted, this was something i used to check the network
	print("Networks Setup: Successful")

	#######################################################################################################################
	# RandomWalks and output processing

	print("Positive Trail Analysis")
	PosWalks = RandomTrail(PosEdges, nWalks, Control=False, Positive=True, minimumTrailLength=minimumTrailLength)
	print("Positive Trail Analysis (Control Data)")
	CPosWalks = RandomTrail(PosEdges, nWalks, Control=True, Positive=True, minimumTrailLength=minimumTrailLength)
	print("Negative Trail Analysis")
	NegWalks = RandomTrail(NegEdges, nWalks, Control=False, Positive=False, minimumTrailLength=minimumTrailLength)
	print("Negative Trail Analysis (Control Data)")
	CNegWalks = RandomTrail(NegEdges, nWalks, Control=True, Positive=False, minimumTrailLength=minimumTrailLength)

	print("Walks: Completed")
	#######################################################################################################################

	PosData = edgetally(PosWalks, PosNetworkFinal)
	NegData = edgetally(NegWalks, NegNetworkFinal)

	CPosData = edgetally(CPosWalks, PosNetworkFinal)
	CNegData = edgetally(CNegWalks, NegNetworkFinal)

	print("Trails Step Splitting and Tallying: Completed")

	#######################################################################################################################
	# Get metrics

	def ChangePercent(df1, df2, Positive):
		# Merge Basal and Biological runs then determine Change(%) from basal network
		df3 = df1.merge(df2, on=['Kinase', 'Substrate', 'Phosphosite', 'Substrate_effect', 'INVLog2FoldChange',
								'Log2FoldChange', 'FoldChange', 'INVFoldChange'], how='outer', suffixes=['_basal', '_biological'])

		df3['Change (%)'] = df3['TotalWalks_biological'] / df3['TotalWalks_basal'] * 100 - 100

		df3 = df3[df3['Change (%)'] > 5]

		# Inverse Negative Trail Change(%) for visualisation on a single network map
		if not Positive:
			df3['Change (%)'] = -df3['Change (%)']

		return df3


	PosFinal = ChangePercent(CPosData, PosData, Positive=True)
	NegFinal = ChangePercent(CNegData, NegData, Positive=False)

	# Merge to final stage networks for visualisation, should be no conflicting rows.
	NetworkFinal = PosFinal.merge(NegFinal, how='outer')

	########################################################################################################################
	outputColumns = ['Kinase', 'Substrate', 'Phosphosite', 'Substrate_effect', 'Log2FoldChange', 'Change (%)']
	columnNameDict = {
		'Kinase': 'Kinase', 
		'Substrate': 'Substrate',
		'Phosphosite': 'Phosphosite', 
		'Substrate_effect': 'SubstrateEffect', 
		'Log2FoldChange': 'Log2FoldChange', 
		'Change (%)': 'Change (%)'
	}

	if edgeUsage:
		outputColumns += ['TotalWalks_basal', 'TotalWalks_biological']
		columnNameDict.update({
			'TotalWalks_basal': 'ControlEdgeUsage',
			'TotalWalks_biological': 'TreatedEdgeUsage'
			}
		)
		
	NetworkFinal = NetworkFinal[outputColumns]
	NetworkFinal = NetworkFinal.rename(columns=columnNameDict)

	# Output for Cytoscape
	NetworkFinal.to_csv(outputPath)

