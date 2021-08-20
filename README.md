# 🗺 MAPPINGS v0.0.1

## Mapping and Analysis of Phosphorylation Pathways Identified through Network/Graph Signalling

Mappings is a tool for blah blah. 

It analyses kinexus chip data to find..

Maybe put a picture here or something. The sky is the limit.

First described by our names here: (Not the real article, but just showing you can put links)

[Network analysis of large phospho-signalling datasets: application to Plasmodium-erythrocyte interactions](https://www.biorxiv.org/content/10.1101/2021.05.07.443051v1)

and it looked pretty good doing it!

![Alt text: complex network structures](https://www.biorxiv.org/content/biorxiv/early/2021/05/07/2021.05.07.443051/F2.large.jpg?width=800&height=600&carousel=1)

Designed and programmed with love by Dr. Jack Adderley and Finn O'Donoghue.

## Installation

	pip install mappings

## Usage

	mappings [OPTIONS] ARRAY_DATA_PATH OUTPUT_PATH

or 

	python -m mappings [OPTIONS] ARRAY_DATA_PATH OUTPUT_PATH

### Options

	  --nwalks INTEGER                Number of walks.
	  --connection_network_path PATH  Network of known phosphorylation connections.

## Input / Output Specification

### Array Data
Sort of comes from kinexus.

CSV file with headers:
 - Uniprot ID
 - Protein
 - Phospho Site (Human),
 - UMean
 - UMean Error (%)
 - TMean
 - TMean Error (%)

### Output Data
For use in Cytoscape or some other analysis program.

CSV file with headers:

- Kinase
- Substrate
- cdf_x
- INVLog2FoldChange 
- ...etc

### Connection  Network
Accumulated from literature reports. Updated version may be available under `data/input/NetworkComplete.csv`
Please email the authors, or submit a pull request to update this file with any new data.

CSV file with headers:
- Phosphosite
- Kinase_uniprot_ID
- Substrate_uniprot_ID
- SubID_phosphosite
- Substrate_effect
- Kinase
- Substrate

## Publications
 - ...et al. 2021
 - [Review by highly respected bioinformatics group et al., 2022](https://www.google.com/search?q=most+important+bioinformatics+tools+of+all+time)