import networkx as nx


def NetworkasDiGraph(PositiveNetwork, NegativeNetwork):

	PosDiGraph = nx.from_pandas_edgelist(PositiveNetwork, source='Kinase',
										 target='Substrate', edge_attr=['Phosphosite', 'Substrate_effect',
																		'Log2FoldChange', 'INVLog2FoldChange',
																		'INVFoldChange', 'FoldChange', 'cdf'],
										 create_using=nx.DiGraph())

	NegDiGraph = nx.from_pandas_edgelist(NegativeNetwork, source='Kinase',
										 target='Substrate', edge_attr=['Phosphosite', 'Substrate_effect',
																		'Log2FoldChange', 'INVFoldChange',
																		'FoldChange', 'INVLog2FoldChange', 'cdf'],
										 create_using=nx.DiGraph())

	PosNetworkFinal = nx.to_pandas_edgelist(PosDiGraph)
	NegNetworkFinal = nx.to_pandas_edgelist(NegDiGraph)

	PosNetworkFinal.rename(inplace=True, columns={'source': 'Kinase', 'target': 'Substrate'})
	NegNetworkFinal.rename(inplace=True, columns={'source': 'Kinase', 'target': 'Substrate'})

	# Setup of directional walks using positive or negative changes in source datasets
	PosEdges = PosDiGraph.copy()
	for edge in PosDiGraph.edges():
		if PosDiGraph.get_edge_data(*edge)["Log2FoldChange"] < 0:
			PosEdges.remove_edge(*edge)

	NegEdges = NegDiGraph.copy()
	for edge in NegDiGraph.edges():
		if NegDiGraph.get_edge_data(*edge)["INVLog2FoldChange"] < 0:
			NegEdges.remove_edge(*edge)

	return PosEdges, NegEdges, PosNetworkFinal, NegNetworkFinal
