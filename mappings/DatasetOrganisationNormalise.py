from mappings.getFoldChangeCDF import getFoldChangeCDF
import pandas as pd
import numpy as np

def DatasetOrganisationNormalise(Data, LowSignalCutOff, ErrorThreshold):
	# Rename columns to easier names
	columnNameDict = {
		'UniprotID': 'UniprotID', 
		'AntibodyTarget': 'Protein', 
		'Phosphosite': 'Phosphosite', 
		'ControlMean': 'URaw', 
		'ControlError(%)': 'UError', 
		'TreatedMean': 'IRaw', 
		'TreatedError(%)': 'IError'
	}

	Data = Data.rename(columns = columnNameDict)

	# Remove Low intensity signals (If neither of the signals are above 1000 units)
	Data = Data[(Data['URaw'] >= LowSignalCutOff) | (Data['IRaw'] >= LowSignalCutOff)]

	# Identify signals where the total error is greater than set threshold

	Data['PercentCFC'] = Data['IRaw'] / Data['URaw'] * 100 - 100
	Data['InversePercentCFC'] = Data['URaw'] / Data['IRaw'] * 100 - 100

	conditions = [
		(Data['PercentCFC'] >= 0) & (Data['PercentCFC'] * ErrorThreshold > (Data['UError'] + Data['IError'])),
		(Data['PercentCFC'] >= 0) & (Data['PercentCFC'] * ErrorThreshold <= (Data['UError'] + Data['IError'])),
		(Data['PercentCFC'] < 0) & (Data['InversePercentCFC'] * ErrorThreshold > (Data['UError'] + Data['IError'])),
		(Data['PercentCFC'] < 0) & (Data['InversePercentCFC'] * ErrorThreshold <= (Data['UError'] + Data['IError']))]

	choices = ['Low', 'High', 'Low', 'High']
	Data['ErrorVerdict'] = np.select(conditions, choices)

	# Remove these high error to change ratio signals
	Data = Data[Data['ErrorVerdict'].str.contains("Low", case=False, na=False)]

	# Remove special characters from Phosphosite column
	Data = Data.replace("\+", ",", regex=True)  # replaces + with , \ needed as + is a special character

	# Split dual + triple phosphosite signals into individual rows with same signal value (Toxo Data)
	DataMulti = Data[Data['Phosphosite'].str.contains(",", case=False, na=False)]  # Multi phosphosites only
	DataMulti['Phosphosite'] = DataMulti['Phosphosite'].str.split(",")  # puts phosphosites into a list using ","
	DataMulti = DataMulti.explode('Phosphosite').reset_index(drop=True)  # splits phosphosite to separate rows
	DataSingle = Data[~Data['Phosphosite'].str.contains(",", case=True, na=False)]  # Single phosphosite only
	Data = [DataMulti, DataSingle]
	Data = pd.concat(Data).reset_index(drop=True)  # join multi and single and reset index

	# Creates Reference for mapping to network
	Data['Concat'] = Data['UniprotID'].map(str) + '/' + Data['Phosphosite'].map(str)

	Data['Log2FoldChange'] = np.log2(Data['IRaw'] / Data['URaw'])

	PanData = Data[Data['Phosphosite'].str.contains("Pan", na=False)]
	PhosData = Data[~Data['Phosphosite'].str.contains("Pan", na=False)]

	# If multiple values are available for a given phosphorylation site/protein average values
	PhosData = PhosData.groupby(['Concat'], as_index=False).agg(
		{'Log2FoldChange': 'mean', 'UniprotID': 'first', 'Protein': 'first',
		 'Phosphosite': 'first'})

	PanData = PanData.groupby(['Concat'], as_index=False).agg(
		{'Log2FoldChange': 'mean', 'UniprotID': 'first', 'Protein': 'first',
		 'Phosphosite': 'first'})

	# Merge Pan and Phospho dataframes
	Data = PhosData.merge(PanData, on='UniprotID', how='left')
	Data.fillna(0, inplace=True)
	Data.rename(columns={'Protein_x': 'Protein', 'Phosphosite_x': 'Phosphosite'}, inplace=True)

	#  Adjust Phospho-signal change by Pan-specific signal change (Normalisation to protein amount)
	Data['Log2FoldChange'] = Data['Log2FoldChange_x'] - Data['Log2FoldChange_y']

	# Create Fold Change column
	Data['FoldChange'] = 2 ** Data['Log2FoldChange']
	# Create INV for negative runs
	Data['INVLog2FoldChange'] = 1 / Data['Log2FoldChange']
	Data['INVFoldChange'] = 1 / Data['FoldChange']

	# Creates Reference for mapping to network
	Data['SubID_phosphosite'] = Data['UniprotID'].map(str) + '/' + Data['Phosphosite'].map(str)
	Data.drop(['Concat_x', 'Log2FoldChange_x', 'Concat_y','Log2FoldChange_y', 'Protein_y', 'Phosphosite_y'], axis=1,
			  inplace=True)

	# Determine CDF value for each edge (used in trail termination chance)
	NegDFwithCDF = getFoldChangeCDF(Data[Data['Log2FoldChange'] < 0], Positive=False)
	PosDFwithCDF = getFoldChangeCDF(Data[Data['Log2FoldChange'] >= 0], Positive=True)

	return PosDFwithCDF, NegDFwithCDF