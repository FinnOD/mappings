import pandas as pd

def Merger(Network, PosDataCorrected, NegDataCorrected):

	PosMappedNetwork = pd.merge(PosDataCorrected, Network, how='right', on='SubID_phosphosite')  # merge network to data

	PosMappedNetwork.dropna(subset=['Log2FoldChange'], inplace=True)  # remove unlinked data
	PosMappedNetwork = PosMappedNetwork.drop(['SubID_phosphosite', 'UniprotID', 'Protein', 'Phosphosite_x'], axis=1)
	PosMappedNetwork = PosMappedNetwork[
		['Kinase', 'Substrate', 'Phosphosite_y', 'Substrate_effect', 'Log2FoldChange',
		 'Kinase_uniprot_ID', 'Substrate_uniprot_ID', 'FoldChange', 'cdf']]
	PosMappedNetwork = PosMappedNetwork.rename({'Phosphosite_y': 'Phosphosite'}, axis=1)

	# Remove duplicate rows
	PosMappedNetwork['Concat'] = PosMappedNetwork['Kinase_uniprot_ID'].map(str) + '/' + \
							  PosMappedNetwork['Substrate_uniprot_ID'].map(str) + '/' + \
							  PosMappedNetwork['Phosphosite'].map(str)  # make reference column

	PosMappedNetwork = PosMappedNetwork.drop_duplicates(subset=['Concat'], keep='first')  # remove duplicate, keep first
	PosMappedNetwork = PosMappedNetwork.drop(['Concat'], axis=1)

	PosMappedNetwork['INVLog2FoldChange'] = -PosMappedNetwork['Log2FoldChange']  # INV reference for negative walks
	PosMappedNetwork['INVFoldChange'] = 1 / PosMappedNetwork['FoldChange']
	
########################################################################################################################
	NegMappedNetwork = pd.merge(NegDataCorrected, Network, how='right', on='SubID_phosphosite')  # merge network to data

	NegMappedNetwork.dropna(subset=['Log2FoldChange'], inplace=True)  # remove unlinked data
	NegMappedNetwork = NegMappedNetwork.drop(['SubID_phosphosite', 'UniprotID', 'Protein', 'Phosphosite_x'], axis=1)
	NegMappedNetwork = NegMappedNetwork[
		['Kinase', 'Substrate', 'Phosphosite_y', 'Substrate_effect', 'Log2FoldChange',
		 'Kinase_uniprot_ID', 'Substrate_uniprot_ID', 'FoldChange', 'cdf']]
	NegMappedNetwork = NegMappedNetwork.rename({'Phosphosite_y': 'Phosphosite'}, axis=1)

	# Remove duplicate rows
	NegMappedNetwork['Concat'] = NegMappedNetwork['Kinase_uniprot_ID'].map(str) + '/' + \
							  NegMappedNetwork['Substrate_uniprot_ID'].map(str) + '/' + \
							  NegMappedNetwork['Phosphosite'].map(str)  # make reference column

	NegMappedNetwork = NegMappedNetwork.drop_duplicates(subset=['Concat'], keep='first')  # remove duplicate, keep first
	NegMappedNetwork = NegMappedNetwork.drop(['Concat'], axis=1)

	NegMappedNetwork['INVLog2FoldChange'] = -NegMappedNetwork['Log2FoldChange']  # INV reference for negative walks
	NegMappedNetwork['INVFoldChange'] = 1 / NegMappedNetwork['FoldChange']
########################################################################################################################
	# Identify the largest fold change for all multi-edges between two nodes for DiGraph setup
	PosNetwork = PosMappedNetwork.sort_values('Log2FoldChange', ascending=False)
	PosNetwork = PosNetwork[~PosNetwork.duplicated(subset=['Kinase', 'Substrate'], keep='first')]
	NegNetwork = NegMappedNetwork.sort_values('INVLog2FoldChange', ascending=False)
	NegNetwork = NegNetwork[~NegNetwork.duplicated(subset=['Kinase', 'Substrate'], keep='first')]

	return PosNetwork, NegNetwork
