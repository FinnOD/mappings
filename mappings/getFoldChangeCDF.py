import pandas as pd


def getFoldChangeCDF(FCdf, foldChangeLabel='FoldChange', Positive=True):
	stats_df = FCdf.groupby(foldChangeLabel)[foldChangeLabel].agg('count').pipe(pd.DataFrame).rename(columns={foldChangeLabel: 'frequency'})

	# PDF
	stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])

	# CDF
	if Positive:
		stats_df['cdf'] = stats_df['pdf'].cumsum()
	else:
		stats_df['cdf'] = 1 - stats_df['pdf'].cumsum()

	stats_df = stats_df.reset_index()

	return FCdf.join(stats_df.set_index(foldChangeLabel), on=foldChangeLabel)
