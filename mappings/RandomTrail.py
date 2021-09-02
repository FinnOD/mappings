import itertools
import random
from tqdm import tqdm
import time
import click
#######################################################################################################################
# RandomTrail function (Walks as (N,N,N,N))

def RandomTrail(g, nwalks, Control, Positive, minimumTrailLength, abortTime=5):

	pbar = tqdm(total=nwalks, desc='Running Random Trails', unit=' trails')  # Progress Bar
	VTX = g.nodes()  # defines VTX as all of the nodes in the graph
	walks = list()
	j = 0
	
	updateTime = time.time()

	while j < nwalks:

		walk = list()
		visited = list()

		for step in itertools.count(start=1):  # for each step of the trail

			if step == 1:  # if this is the first step

				node = random.sample(VTX, 1)[0]  # select a random node from the network

			else:  # if this is not the first step of a trail use last node from previous step
				# Determine chance for trail termination based on edge Fold change value last used

				if Control:
					TerminationChance = 0.20

				if not Control:
					TerminationChance = 0.20 * (1 - g.get_edge_data(*selectededge)['cdf'])

				if random.random() < TerminationChance:
					break

				else:
					node = nextnode  # select last node after previous step

			walkelements = node

			adjacent = list(g.edges(node))  # paths out from the node
#######################################################################################################################
			# assesses if the substrate effect code from the last step was negative, if so end the walk

			if step != 1:  # if not the first step of walk and last edge walked substrate effect code = '-' break

				if g.get_edge_data(*selectededge)['Substrate_effect'] == "-":

					walk.append(walkelements)
					break
#######################################################################################################################
			# Stop walks from rewalking steps already used and end walks if the pathway is now a dead end

			if len(visited) > 0:  # remove visited edges from the options

				adjacent = [x for x in adjacent if x not in visited]

			if len(adjacent) == 0:  # if now a dead end after removing visited edges, end walk

				walk.append(walkelements)
				break
#######################################################################################################################
			elif len(adjacent) == 1:  # else if there is only one edge option?

				selectededge = adjacent[0]
				nextnode = selectededge[1]  # Use the edge

#######################################################################################################################
			else:  # else there is more than 1 edge to choose from, therefore a weighted decision is required

				# adding weighting to the edges based on FoldChange
				if not Control:  # If this is not a Basal/Control network trails analysis
					prob = list()

					# for each adjacent edge get the associated FoldChanges
					for i in range(0, len(adjacent)):
						if Positive:
							prob.append(g.get_edge_data(node, adjacent[i][1])['FoldChange'])
						else:
							prob.append(g.get_edge_data(node, adjacent[i][1])['INVFoldChange'])

					totalprob = sum(prob)
					if totalprob == 0:  # if the edge probabilities = 0 ie two or more edges without positive weights
						walk.append(walkelements)  # end walk

					else:  # else the edge selection is weighted by the FoldChange values
						selectededge = random.choices(adjacent, weights=prob, k=1)[0]
						nextnode = selectededge[1]  # the second node in the edge (used in next step of walk)

				else:  # If this is a Basal/Control network trails analysis then edge choice is random

					selectededge = random.choices(adjacent, k=1)[0]
					nextnode = selectededge[1]
#######################################################################################################################

			visited.append(selectededge)

			walk.append(walkelements)  # defines the walk as the sum of the walk elements

		if len(walk) >= minimumTrailLength:
			walks.append(walk)

			j = j + 1
			pbar.update(1)

			updateTime = time.time()

		else:
			if time.time() - updateTime > abortTime:
				pbar.close()
				click.echo('\n')
				raise click.UsageError(f'Trails failed to accumulate. Try lowering the minimum trail length using the -M flag. Currently set to {minimumTrailLength}.')

	pbar.close()

	return walks



