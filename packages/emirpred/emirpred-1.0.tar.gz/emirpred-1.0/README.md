# **EmiRPred**
A computational tool for predicting exosomal and non-exosomal miRNA
## Introduction
EmiRPred is a tool for the classifcation of miRNA into exosomal and non-exosomal. It uses similarity-based methods (BLAST and MERCI for motif-search) combined with Extra Tree Classifier built on the best performing compoisition-based features extracted using One hot encoding, Term Frequency - Inverse Document Frequency, and Reverse Complement RNA strand compositions. EmiRPred is also available as a web-server at https://webs.iiitd.edu.in/raghava/emirpred. Please read/cite the content about EmiRPred for complete information including algorithm behind the approach.


## Standalone
The Standalone version of EmiRPred is written in python3 and following libraries are necessary for the successful run:
- scikit-learn=1.2.2
- Pandas
- Numpy
- Joblib
- Argparse

No additional package/tool is required for model = 1 (default model), however for model = 2, please download blast from https://blast.ncbi.nlm.nih.gov/doc/blast-help/downloadblastdata.html


## Minimum USAGE
To know about the available option for the standlone, type the following command:
```
emirpred -h
```
To run the example, type the following command:
```
emirpred -f example_input.fa -o output
```
Here, -f argument is to enter the input file in Fasta format and -o argument is for giving the path to the output directory. By default, the package uses model (-m) = 1 which employs only ML algorithm (Extra Tree Classifier) to classify the miRNA sequences, which generates a prediction file "classification_ML.csv" in the specified output directory. If model (-m) = 2 is selected, then the hybrid model is employed (ML + MERCI + BLAST) to classify the miRNA sequences, which generates a prediction file "classification_hybrid.csv" in the specified output directory.

## Full Usage
```
usage: emirpred [-h] --file FILE --output OUTPUT [--model MODEL] [--threshold THRESHOLD]
```
```
Please provide following arguments for successful run
required arguments:
  --file FILE, -f FILE                   Path to fasta file
  --output OUTPUT, -o OUTPUT             Path to output

optional arguments:

  --model MODEL, -m MODEL                Model selection: 1 for ML only, 2 for ML + BLAST + MERCI (By default model = 1)
  --threshold THRESHOLD, -t THRESHOLD    Threshold for classification (can be any value between 0-1 for model = 1 (by default = 0.5) and 0-2 for model = 2 (by default = 0.52))

For help:
  -h, --help            show this help message and exit

```

**Input File:** It allow users to provide input in FASTA format.

**Output File:** Program will save the results to this folder

**Model:** User can pick which model to run, model = 1 runs only ML model (ET classifier), whereas model = 2 runs hybrid model (ML + BLAST + MERCI), by default the tool runs model = 1

**Threshold:** User can provide threshold for classification (can be any value between 0-1 for model = 1 (by default = 0.5) and 0-2 for model = 2 (by default = 0.52))


EmiRPred Package Files
=======================
It contantain following files, brief description of these files given below

INSTALLATION                    : Installations instructions

LICENSE                         : License information

README.md                       : This file provide information about this package

emirpred_et_model.pkl           : This file contains the pickled version of model

emirpred.py                     : Main python program

example_input.fa                : Example file contain nucleotide sequences in FASTA format

blast_db                        : Database for BLAST search

MERCI_motif_locator.pl          : To locate exosomal motifs within the query sequences