# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 12:42:37 2020

@author: Megha Mathur
"""
import argparse  
import warnings
import os
from argparse import RawTextHelpFormatter
warnings.filterwarnings('ignore')
parser = argparse.ArgumentParser(description='NFRNA....Please provide following arguments to proceed',formatter_class=RawTextHelpFormatter)
nf_path = os.path.dirname(__file__)
## Read Arguments from command
parser.add_argument("-i", "--input", type=str,required=True,help="Input: protein or peptide sequence in FASTA format")
parser.add_argument("-o", "--output", type=str,help="Output File name")
parser.add_argument("-ft", "--feature",required=True,type=str,
                     help="Select among various features and include _NT,_CT,_REST,_SPLIT after feature name for N-Terminal,C-Terminal,Reamining of N-terminal and C-Terminal and for splitted sequence respectively.\n"
                    "\n"
                    "ALL_COMP : all composition based features\n"
	  "ALL_CORR : all correlation based features\n"
	  "ALL_BIN: all binary profile based features\n"
                    "CDK : kmer composition\n"
                    "RDK : Reverse Compliment kmer composition\n"                   
                    "DAC : Dinucleotide based auto correlation\n"
                    "DCC : Dinucleotide based cross correlation\n"
                    "DACC : Dinucleotide based auto cross correlation\n"
                    "PDNC :  Pseudo dinucleotide composition\n"
                    "PC_PDNC : parallel correlation pseudo dinucleotide composition\n"
                    "SC_PDNC : Serial correlation pseudo dinucleotide composition\n"
                    "NRI : Nucleotide repeat index\n"
                    "ES : Sequence level entropy of whole sequence\n"
                    "EN : Nucleotide level entropy of whole sequence\n"
                    "DDN : Distance Distribution of whole sequence\n"
                    "BPD : Binary profile dinucleotide\n"
                    "BPM : Binary profile Monotide\n"
                    "BP_DP : Dinucleotide properties")
parser.add_argument("-k","--kvalue",type=int, help="Enter the k value and by default it is set to 2")
parser.add_argument("-n","--nvalue",type=int, help="Enter the n value")
parser.add_argument("-c","--cvalue",type=int, help="Enter the c value")
parser.add_argument("-s","--split",type=int, help="Enter the split value")
parser.add_argument("-or","--order",type=int, help="Enter the order value and by default it is set to 1")
parser.add_argument("-p", "--property",type=str,nargs='+',help=" Refer the property list of dipeptides and enter property names having space in between")
parser.add_argument("-l","--lagvalue",type=int, help="Enter the lag value and its default value is 2")
parser.add_argument("-w","--wvalue",type=float, help="Enter the w value and its default value is 0.05")
parser.add_argument("-lm","--lmvalue",type=int, help="Enter the lamada value and its default value is 1")
parser.add_argument("-path","--pythonpath",type=str, help="Enter the python environment path")


args = parser.parse_args()
sequence = args.input
feature = args.feature
feature=feature.upper()
f_list=['ALL_COMP','ALL_CORR','ALL_BIN','CDK','CDK_NT','RDK_NT','RDK_CT','RDK_REST','RDK_SPLIT','CDK_CT','CDK_REST','CDK_SPLIT','RDK','NRI','NRI_NT','NRI_CT','NRI_REST','NRI_SPLIT','DDN','DDN_NT','DDN_CT','DDN_REST','DDN_SPLIT','ES','ES_NT','ES_CT','ES_REST','ES_SPLIT','EN','EN_NT','EN_CT','EN_REST','EN_SPLIT','BPM','BPM_NT','BPM_CT','BPM_REST','BPM_SPLIT','BPD','BPD_NT','BPD_CT','BPD_REST','BPD_SPLIT','BP_DP','BP_DP_NT','BP_DP_CT','BP_DP_REST','BP_DP_SPLIT','DAC','DAC_NT','DAC_CT','DAC_REST','DAC_SPLIT','DACC','DACC_NT','DACC_CT','DACC_REST','DACC_SPLIT','DCC','DCC_NT','DCC_CT','DCC_REST','DCC_SPLIT','PDNC','PDNC_NT','PDNC_CT','PDNC_REST','PDNC_SPLIT','PC_PDNC','PC_PDNC_NT','PC_PDNC_CT','PC_PDNC_REST','PC_PDNC_SPLIT','SC_PDNC','SC_PDNC_NT','SC_PDNC_CT','SC_PDNC_REST','SC_PDNC_SPLIT']
if feature not in f_list:
    print("No Such Feature Exists")
    exit()   
if(args.output==None):
    out="Output.csv"
else:
    out=args.output
if(args.pythonpath==None):
    path='python'
else:
    path=args.pythonpath
# Calling each features
if feature == 'CDK':
    file = open(out,'w')
    file.close()
    if args.kvalue==None:
        k=str(2)
    else:
        k=str(args.kvalue)
    if args.order == None:
        order = str(1)
    else:
        order = str(args.order)
    a = path+" "+nf_path+"/Data/CDK.py "+"-i "+sequence+" -k "+k+" -or "+order+" -o "+out
    os.system(a)
    
if feature == 'RDK':
    file = open(out,'w')
    file.close()
    if args.kvalue==None:
        k=str(2)
    else:
        k=str(args.kvalue)
    a = path+" "+nf_path+"/Data/RDK.py "+"-i "+sequence+" -k "+k+" -o "+out
    os.system(a)
    
if feature == 'ALL_COMP':
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.lmvalue == None:
        lm = str(1)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.order == None:
        order = str(1)
    else:
        order = str(args.order)
    if args.kvalue==None:
        k=str(2)
    else:
        k=str(args.kvalue)
    file = open(out,'w')
    file.close()
    a = path+" "+nf_path+"/Data/K_Mer.py "+"-i "+sequence+" -k "+k+" -or "+order+" -o "+out
    b= path+" "+nf_path+"/Data/NRI.py "+"-i "+sequence+" -o "+out
    c = path+" "+nf_path+"/Data/DDON.py "+"-i "+sequence+" -o "+out
    d= path+" "+nf_path+"/Data/RDK.py "+"-i "+sequence+" -k "+k+" -o "+out
    e = path+" "+nf_path+"/Data/ENT.py "+"-i "+sequence+" -o "+out
    f = path+" "+nf_path+"/Data/ENT_NL.py "+"-i "+sequence+" -o "+out
    k1 = path+" "+nf_path+"/Data/psednc.py "+"-i "+sequence+" -w "+w+" -k "+k+" -lm "+lm+" -o "+out
    os.system(a)
    os.system(b)
    os.system(c)
    os.system(d)
    os.system(e)
    os.system(f)
    os.system(k1)
if feature == 'ALL_BIN':
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    if args.order == None:
        order = str(1)
    else:
        order = int(args.order)
        order=str(order)
    file = open(out,'w')
    file.close()
    a = path+" "+nf_path+"/Data/BinaryProfile_monotide.py "+"-i "+sequence+" -o "+out
    b= path+" "+nf_path+"/Data/BinaryProfile_dinucleotide.py "+"-i "+sequence+" -o "+out
    c = path+" "+nf_path+"/Data/BinaryProfile_trinucleotide.py "+"-i "+sequence+" -o "+out
    d = path+" "+nf_path+"/Data/dinucleotide_prop.py "+"-i "+sequence+" -or "+order+" -o "+out+" -p"   
    for i in prop:
        j='"'+i+'"'
        d=d+" "+j
    os.system(a)
    os.system(b)
    os.system(c)
    os.system(d)
if feature == 'ALL_CORR':
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.lmvalue == None:
        lm = str(1)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.lagvalue == None:
        lag = str(2)
    else:
        lag = str(args.lagvalue)
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    if args.kvalue==None:
        k=str(2)
    else:
        k=str(args.kvalue)
    file = open(out,'w')
    file.close()
    a = path+" "+nf_path+"/Data/DAC.py "+"-i "+sequence+" -l "+lag+" -o "+out+" -p "
    f = path+" "+nf_path+"/Data/DCC.py "+"-i "+sequence+" -l "+lag+" -o "+out+" -p "
    h = path+" "+nf_path+"/Data/DACC.py "+"-i "+sequence+" -l "+lag+" -o "+out+" -p "
    m = path+" "+nf_path+"/Data/pcpsednc.py "+"-i "+sequence+" -w "+w+" -k "+k+" -o "+out+" -lm "+lm+" -p"
    q = path+" "+nf_path+"/Data/scpsednc.py "+"-i "+sequence+" -w "+w+" -k "+k+" -lm "+lm+" -o "+out+" -p"
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
        f=f+" "+j
        h=h+" "+j
        m=m+" "+j
        q=q+" "+j
    os.system(a)
    os.system(f)
    os.system(h)
    os.system(m)
    os.system(q)
if feature == 'CDK_NT':
    file = open(out,'w')
    file.close()
    if args.kvalue==None:
        k=str(2)
    else:
        k=str(args.kvalue)
    if args.order == None:
        order = str(1)
    else:
        order = str(args.order)
    if args.nvalue==None:
        n = str(len(sequence))  
    else:
        n=str(args.nvalue)
    b = path+" "+nf_path+"/Data/CDK_NT.py "+"-i "+sequence+" -k "+k+" -n "+n+" -or "+order+" -o "+out
    os.system(b)
if feature == 'RDK_NT':
    file = open(out,'w')
    file.close()
    if args.kvalue==None:
        k=str(2)
    else:
        k=str(args.kvalue)
    if args.order == None:
        order = str(1)
    else:
        order = str(args.order)
    if args.nvalue==None:
        n = str(len(sequence))  
    else:
        n=str(args.nvalue)
    b = path+" "+nf_path+"/Data/RDK_NT.py "+"-i "+sequence+" -k "+k+" -n "+n+" -or "+order+" -o "+out
    os.system(b)
if feature == 'RDK_CT':
    file = open(out,'w')
    file.close()
    if args.kvalue==None:
        k=str(2)
    else:
        k=str(args.kvalue)
    if args.order == None:
        order = str(1)
    else:
        order = str(args.order)
    if args.cvalue==None:
        n = str(len(sequence))  
    else:
        n=str(args.cvalue)
    b = path+" "+nf_path+"/Data/RDK_CT.py "+"-i "+sequence+" -k "+k+" -c "+n+" -or "+order+" -o "+out
    os.system(b)
if feature == 'RDK_REST':
    file = open(out,'w')
    file.close()
    if args.kvalue==None:
        k=str(2)
    else:
        k=str(args.kvalue)
    if args.order == None:
        order = str(1)
    else:
        order = str(args.order)
    if args.nvalue==None:
        n = str(0)  
    else:
        n=str(args.nvalue)
    if args.cvalue==None:
        m = str(0)  
    else:
        m=str(args.cvalue)
    b = path+" "+nf_path+"/Data/RDK_REST.py "+"-i "+sequence+" -k "+k+" -n "+n+" -c "+m+" -or "+order+" -o "+out
    os.system(b)
if feature == 'RDK_SPLIT':
    file = open(out,'w')
    file.close()
    if args.kvalue==None:
        k=str(2)
    else:
        k=str(args.kvalue)
    if args.split==None:
        s=str(1)
    else:
        s=str(args.split)
    if args.order == None:
        order = str(1)
    else:
        order = str(args.order)    
    e = path+" "+nf_path+"/Data/RDK_SPLIT.py "+"-i "+sequence+" -k "+k+" -s "+s+" -or "+order+" -o "+out
    os.system(e)
if feature == 'CDK_CT':
    file = open(out,'w')
    file.close()
    if args.kvalue==None:
        k=str(2)
    else:
        k=str(args.kvalue)
    if args.order == None:
        order = str(1)
    else:
        order = str(args.order)
    if args.cvalue==None:
        n = str(len(sequence))  
    else:
        n=str(args.cvalue)
    b = path+" "+nf_path+"/Data/CDK_CT.py "+"-i "+sequence+" -k "+k+" -c "+n+" -or "+order+" -o "+out
    os.system(b)
if feature == 'CDK_REST':
    file = open(out,'w')
    file.close()
    if args.kvalue==None:
        k=str(2)
    else:
        k=str(args.kvalue)
    if args.order == None:
        order = str(1)
    else:
        order = str(args.order)
    if args.nvalue==None:
        n = str(0)  
    else:
        n=str(args.nvalue)
    if args.cvalue==None:
        m = str(0)  
    else:
        m=str(args.cvalue)
    b = path+" "+nf_path+"/Data/CDK_REST.py "+"-i "+sequence+" -k "+k+" -n "+n+" -c "+m+" -or "+order+" -o "+out
    os.system(b)
if feature == 'CDK_SPLIT':
    file = open(out,'w')
    file.close()
    if args.kvalue==None:
        k=str(2)
    else:
        k=str(args.kvalue)
    if args.split==None:
        s=str(1)
    else:
        s=str(args.split)
    if args.order == None:
        order = str(1)
    else:
        order = str(args.order)    
    e = path+" "+nf_path+"/Data/CDK_SPLIT.py "+"-i "+sequence+" -k "+k+" -s "+s+" -or "+order+" -o "+out
    os.system(e)
    
if feature == 'DAC':
    file = open(out,'w')
    file.close()
    if args.lagvalue == None:
        lag = str(2)
    else:
        lag = str(args.lagvalue)
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop= args.property
    a = path+" "+nf_path+"/Data/DAC.py "+"-i "+sequence+" -l "+lag+" -o "+out+" -p "
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'DAC_NT':
    if args.lagvalue == None:
        lag = str(2)
    else:
        lag = str(args.lagvalue)
    if args.nvalue==None:
        n = str(2)  
    else:
        n=str(args.nvalue)
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop= args.property
    a = path+" "+nf_path+"/Data/DAC_NT.py "+"-i "+sequence+" -n "+n+" -l "+lag+" -o "+out+" -p "
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'DAC_CT':
    if args.lagvalue == None:
        lag = str(2)
    else:
        lag = str(args.lagvalue)
    if args.cvalue==None:
        m = str(2)  
    else:
        m=str(args.cvalue)
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop= args.property
    a = path+" "+nf_path+"/Data/DAC_CT.py "+"-i "+sequence+" -c "+m+" -l "+lag+" -o "+out+" -p "
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'DAC_REST':
    if args.lagvalue == None:
        lag = str(2)
    else:
        lag = str(args.lagvalue)
    if args.nvalue==None:
        n = str(0)  
    else:
        n=str(args.nvalue)
    if args.cvalue==None:
        m = str(0)  
    else:
        m=str(args.cvalue)
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop= args.property
    a = path+" "+nf_path+"/Data/DAC_REST.py "+"-i "+sequence+" -n "+n+" -c "+m+" -l "+lag+" -o "+out+" -p "
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'DAC_SPLIT':
    if args.lagvalue == None:
        lag = str(2)
    else:
        lag = str(args.lagvalue)
    if args.split==None:
        s=str(1)
    else:
        s=str(args.split)
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop= args.property
    a = path+" "+nf_path+"/Data/DAC_SPLIT.py "+"-i "+sequence+" -s "+s+" -l "+lag+" -o "+out+" -p "
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'DCC':
    file = open(out,'w')
    file.close()
    if args.lagvalue == None:
        lag = str(2)
    else:
        lag = str(args.lagvalue)
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop= args.property
    a = path+" "+nf_path+"/Data/DCC.py "+"-i "+sequence+" -l "+lag+" -o "+out+" -p "
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'DCC_NT':
    if args.lagvalue == None:
        lag = str(2)
    else:
        lag = str(args.lagvalue)
    if args.nvalue==None:
        n = str(2)  
    else:
        n=str(args.nvalue)
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop= args.property
    a = path+" "+nf_path+"/Data/DCC_NT.py "+"-i "+sequence+" -n "+n+" -l "+lag+" -o "+out+" -p "
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'DCC_CT':
    if args.lagvalue == None:
        lag = str(2)
    else:
        lag = str(args.lagvalue)
    if args.cvalue==None:
        m = str(2) 
    else:
        m=str(args.cvalue)
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop= args.property
    a = path+" "+nf_path+"/Data/DCC_CT.py "+"-i "+sequence+" -c "+m+" -l "+lag+" -o "+out+" -p "
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'DCC_REST':
    if args.lagvalue == None:
        lag = str(2)
    else:
        lag = str(args.lagvalue)
    if args.nvalue==None:
        n = str(0)  
    else:
        n=str(args.nvalue)
    if args.cvalue==None:
        m = str(0)  
    else:
        m=str(args.cvalue)
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop= args.property
    a = path+" "+nf_path+"/Data/DCC_REST.py "+"-i "+sequence+" -n "+n+" -c "+m+" -l "+lag+" -o "+out+" -p "
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'DCC_SPLIT':
    if args.lagvalue == None:
        lag = str(2)
    else:
        lag = str(args.lagvalue)
    if args.split==None:
        s=str(1)
    else:
        s=str(args.split)
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop= args.property
    a = path+" "+nf_path+"/Data/DCC_SPLIT.py "+"-i "+sequence+" -s "+s+" -l "+lag+" -o "+out+" -p "
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'DACC':
    file = open(out,'w')
    file.close()
    if args.lagvalue == None:
        lag = str(2)
    else:
        lag = str(args.lagvalue)
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    a = path+" "+nf_path+"/Data/DACC.py "+"-i "+sequence+" -l "+lag+" -o "+out+" -p "
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'DACC_NT':
    if args.lagvalue == None:
        lag = str(2)
    else:
        lag = str(args.lagvalue)
    if args.nvalue==None:
        n = str(2)  
    else:
        n=str(args.nvalue)
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop= args.property
    a = path+" "+nf_path+"/Data/DACC_NT.py "+"-i "+sequence+" -n "+n+" -l "+lag+" -o "+out+" -p "
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'DACC_CT':
    if args.lagvalue == None:
        lag = str(2)
    else:
        lag = str(args.lagvalue)
    if args.cvalue==None:
        m = str(2)  
    else:
        m=str(args.cvalue)
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop= args.property
    a = path+" "+nf_path+"/Data/DACC_CT.py "+"-i "+sequence+" -c "+m+" -l "+lag+" -o "+out+" -p "
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'DACC_REST':
    if args.lagvalue == None:
        lag = str(2)
    else:
        lag = str(args.lagvalue)
    if args.nvalue==None:
        n = str(0)  
    else:
        n=str(args.nvalue)
    if args.cvalue==None:
        m = str(0)  
    else:
        m=str(args.cvalue)
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop= args.property
    a = path+" "+nf_path+"/Data/DACC_REST.py "+"-i "+sequence+" -n "+n+" -c "+m+" -l "+lag+" -o "+out+" -p "
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'DACC_SPLIT':
    if args.lagvalue == None:
        lag = str(2)
    else:
        lag = str(args.lagvalue)
    if args.split==None:
        s=str(1)
    else:
        s=str(args.split)
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop= args.property
    a = path+" "+nf_path+"/Data/DACC_SPLIT.py "+"-i "+sequence+" -s "+s+" -l "+lag+" -o "+out+" -p "
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)

if feature == 'BPD':
    file = open(out,'w')
    file.close()
    a = path+" "+nf_path+"/Data/BinaryProfile_dinucleotide.py "+"-i "+sequence+" -o "+out
    os.system(a)
if feature == 'BPD_NT':
    if args.nvalue==None:
        n = str(2)  
    else:
        n=str(args.nvalue)
    a = path+" "+nf_path+"/Data/BinaryProfile_dinucleotide_NT.py "+"-i "+sequence+" -n "+n+" -o "+out
    os.system(a)
if feature == 'BPD_CT':
    if args.cvalue==None:
        m = str(2)  
    else:
        m=str(args.cvalue)
    a = path+" "+nf_path+"/Data/BinaryProfile_dinucleotide_CT.py "+"-i "+sequence+" -c "+m+" -o "+out
    os.system(a)
if feature == 'BPD_REST':
    if args.nvalue==None:
        n = str(0)  
    else:
        n=str(args.nvalue)
    if args.cvalue==None:
        m = str(0)  
    else:
        m=str(args.cvalue)
    a = path+" "+nf_path+"/Data/BinaryProfile_dinucleotide_REST.py "+"-i "+sequence+" -n "+n+" -c "+m+" -o "+out
    os.system(a)
if feature == 'BPD_SPLIT':
    if args.split==None:
        s = str(1)  
    else:
        s=str(args.split)
    a = path+" "+nf_path+"/Data/BinaryProfile_dinucleotide_SPLIT.py "+"-i "+sequence+" -s "+s+" -o "+out
    os.system(a)
if feature=='BPM':
    file = open(out,'w')
    file.close()
    a=path+" "+nf_path+"/Data/BinaryProfile_monotide.py "+"-i "+sequence+" -o "+out
    os.system(a)
if feature == 'BPM_NT':
    if args.nvalue==None:
        n = str(2)  
    else:
        n=str(args.nvalue)
    a = path+" "+nf_path+"/Data/BinaryProfile_mononucleotide_NT.py "+"-i "+sequence+" -n "+n+" -o "+out
    os.system(a)
if feature == 'BPM_CT':
    if args.cvalue==None:
        m = str(2)  
    else:
        m=str(args.cvalue)
    a = path+" "+nf_path+"/Data/BinaryProfile_mononucleotide_CT.py "+"-i "+sequence+" -c "+m+" -o "+out
    os.system(a)
if feature == 'BPM_REST':
    if args.nvalue==None:
        n = str(0)  
    else:
        n=str(args.nvalue)
    if args.cvalue==None:
        m = str(0)  
    else:
        m=str(args.cvalue)
    a = path+" "+nf_path+"/Data/BinaryProfile_mononucleotide_REST.py "+"-i "+sequence+" -n "+n+" -c "+m+" -o "+out
    os.system(a)
if feature == 'BPM_SPLIT':
    if args.split==None:
        s = str(1)  
    else:
        s=str(args.split)
    a = path+" "+nf_path+"/Data/BinaryProfile_mononucleotide_SPLIT.py "+"-i "+sequence+" -s "+s+" -o "+out
    os.system(a)
if feature=='BPT':
    file = open(out,'w')
    file.close()
    a=path+" "+nf_path+"/Data/BinaryProfile_trinucleotide.py "+"-i "+sequence+" -o "+out
    os.system(a)
if feature == 'BPT_NT':
    if args.nvalue==None:
        n = str(2)
    else:
        n=str(args.nvalue)
    a = path+" "+nf_path+"/Data/BinaryProfile_trinucleotide_NT.py "+"-i "+sequence+" -n "+n+" -o "+out
    os.system(a)
if feature == 'BPT_CT':
    if args.cvalue==None:
        m = str(2)
    else:
        m=str(args.cvalue)
    a = path+" "+nf_path+"/Data/BinaryProfile_trinucleotide_CT.py "+"-i "+sequence+" -c "+m+" -o "+out
    os.system(a)
if feature == 'BPT_REST':
    if args.nvalue==None:
        n = str(0)
    else:
        n=str(args.nvalue)
    if args.cvalue==None:
        m = str(0)
    else:
        m=str(args.cvalue)
    a = path+" "+nf_path+"/Data/BinaryProfile_trinucleotide_REST.py "+"-i "+sequence+" -n "+n+" -c "+m+" -o "+out
    os.system(a)
if feature == 'BPT_SPLIT':
    if args.split==None:
        s = str(1)
    else:
        s=str(args.split)
    a = path+" "+nf_path+"/Data/BinaryProfile_trinucleotide_SPLIT.py "+"-i "+sequence+" -s "+s+" -o "+out
    os.system(a)

if feature == 'PDNC':
    file = open(out,'w')
    file.close()
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.lmvalue == None:
        lm = str(3)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.kvalue == None:
        k = str(2)
    else:
        k = int(args.kvalue)
        k=str(k)        
    a = path+" "+nf_path+"/Data/psednc.py "+"-i "+sequence+" -w "+w+" -k "+k+" -lm "+lm+" -o "+out
    os.system(a)
if feature == 'PDNC_NT':
    if args.nvalue==None:
        n = str(2)  
    else:
        n=str(args.nvalue)
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.lmvalue == None:
        lm = str(3)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.kvalue == None:
        k = str(2)
    else:
        k = int(args.kvalue)
        k=str(k)        
    a = path+" "+nf_path+"/Data/psednc_NT.py "+"-i "+sequence+" -w "+w+" -n "+n+" -k "+k+" -lm "+lm+" -o "+out
    os.system(a)
if feature == 'PDNC_CT':
    if args.cvalue==None:
        m = str(2)  
    else:
        m=str(args.cvalue)
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.lmvalue == None:
        lm = str(3)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.kvalue == None:
        k = str(2)
    else:
        k = int(args.kvalue)
        k=str(k)        
    a = path+" "+nf_path+"/Data/psednc_CT.py "+"-i "+sequence+" -w "+w+" -c "+m+" -k "+k+" -lm "+lm+" -o "+out
    os.system(a)
if feature == 'PDNC_REST':
    if args.nvalue==None:
        n = str(0)  
    else:
        n=str(args.nvalue)
    if args.cvalue==None:
        m = str(0)  
    else:
        m=str(args.cvalue)
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.lmvalue == None:
        lm = str(3)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.kvalue == None:
        k = str(2)
    else:
        k = int(args.kvalue)
        k=str(k)        
    a = path+" "+nf_path+"/Data/psednc_REST.py "+"-i "+sequence+" -w "+w+" -n "+n+" -c "+m+" -k "+k+" -lm "+lm+" -o "+out
    os.system(a)
if feature == 'PDNC_SPLIT':
    if args.split==None:
        s = str(1)  
    else:
        s=str(args.split)
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.lmvalue == None:
        lm = str(3)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.kvalue == None:
        k = str(2)
    else:
        k = int(args.kvalue)
        k=str(k)        
    a = path+" "+nf_path+"/Data/psednc_SPLIT.py "+"-i "+sequence+" -w "+w+" -s "+s+" -k "+k+" -lm "+lm+" -o "+out
    os.system(a)

if feature == 'PC_PDNC':
    file = open(out,'w')
    file.close()
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.lmvalue == None:
        lm = str(1)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.kvalue == None:
        k = str(2)
    else:
        k = int(args.kvalue)
        k=str(k)  
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    a = path+" "+nf_path+"/Data/pcpsednc.py "+"-i "+sequence+" -w "+w+" -k "+k+" -o "+out+" -lm "+lm+" -p"
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'PC_PDNC_NT':
    if args.nvalue==None:
        n = str(2)  
    else:
        n=str(args.nvalue)
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.lmvalue == None:
        lm = str(1)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.kvalue == None:
        k = str(2)
    else:
        k = int(args.kvalue)
        k=str(k)  
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    a = path+" "+nf_path+"/Data/pcpsednc_NT.py "+"-i "+sequence+" -w "+w+" -n "+n+" -k "+k+" -o "+out+" -lm "+lm+" -p"
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'PC_PDNC_CT':
    if args.cvalue==None:
        m = str(2)  
    else:
        m=str(args.cvalue)
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.lmvalue == None:
        lm = str(1)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.kvalue == None:
        k = str(2)
    else:
        k = int(args.kvalue)
        k=str(k)  
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    a = path+" "+nf_path+"/Data/pcpsednc_CT.py "+"-i "+sequence+" -w "+w+" -c "+m+" -k "+k+" -o "+out+" -lm "+lm+" -p"
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a) 
if feature == 'PC_PDNC_REST':
    if args.nvalue==None:
        n = str(0)  
    else:
        n=str(args.nvalue)
    if args.cvalue==None:
        m = str(0)  
    else:
        m=str(args.cvalue)
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.lmvalue == None:
        lm = str(1)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.kvalue == None:
        k = str(2)
    else:
        k = int(args.kvalue)
        k=str(k)  
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    a = path+" "+nf_path+"/Data/pcpsednc_REST.py "+"-i "+sequence+" -w "+w+" -n "+n+" -c "+m+" -k "+k+" -o "+out+" -lm "+lm+" -p"
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a) 
if feature == 'PC_PDNC_SPLIT':
    if args.split==None:
        s = str(1)  
    else:
        s=str(args.split)
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.lmvalue == None:
        lm = str(1)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.kvalue == None:
        k = str(2)
    else:
        k = int(args.kvalue)
        k=str(k)  
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    a = path+" "+nf_path+"/Data/pcpsednc_SPLIT.py "+"-i "+sequence+" -w "+w+" -s "+s+" -k "+k+" -o "+out+" -lm "+lm+" -p"
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)

if feature == 'SC_PDNC':
    file = open(out,'w')
    file.close()
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.lmvalue == None:
        lm = str(1)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.kvalue == None:
        k = str(2)
    else:
        k = int(args.kvalue)
        k=str(k)  
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    a = path+" "+nf_path+"/Data/scpsednc.py "+"-i "+sequence+" -w "+w+" -k "+k+" -lm "+lm+" -o "+out+" -p"
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'SC_PDNC_NT':
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.nvalue == None:
        n = str(2)
    else:
        n = str(args.nvalue)
    if args.lmvalue == None:
        lm = str(1)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.kvalue == None:
        k = str(2)
    else:
        k = int(args.kvalue)
        k=str(k)  
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    a = path+" "+nf_path+"/Data/scpsednc_NT.py "+"-i "+sequence+" -w "+w+" -n "+n+" -k "+k+" -lm "+lm+" -o "+out+" -p"
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'SC_PDNC_CT':
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.cvalue == None:
        m = str(2)
    else:
        m = str(args.cvalue)
    if args.lmvalue == None:
        lm = str(1)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.kvalue == None:
        k = str(2)
    else:
        k = int(args.kvalue)
        k=str(k)  
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    a = path+" "+nf_path+"/Data/scpsednc.py_CT "+"-i "+sequence+" -w "+w+" -c "+m+" -k "+k+" -lm "+lm+" -o "+out+" -p"
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a) 
if feature == 'SC_PDNC_REST':
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.nvalue == None:
        n = str(0)
    else:
        n = str(args.nvalue)
    if args.cvalue == None:
        m = str(0)
    else:
        m = str(args.cvalue)
    if args.lmvalue == None:
        lm = str(1)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.kvalue == None:
        k = str(2)
    else:
        k = int(args.kvalue)
        k=str(k)  
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    a = path+" "+nf_path+"/Data/scpsednc_REST.py "+"-i "+sequence+" -w "+w+" -n "+n+" -c "+m+" -k "+k+" -lm "+lm+" -o "+out+" -p"
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature == 'SC_PDNC_SPLIT':
    if args.wvalue == None:
        w = str(0.05)
    else:
        w = float(args.wvalue)
        w=str(w)
    if args.split == None:
        s = str(1)
    else:
        s = str(args.split)
    if args.lmvalue == None:
        lm = str(1)
    else:
        lm = int(args.lmvalue) 
        lm=str(lm)
    if args.kvalue == None:
        k = str(2)
    else:
        k = int(args.kvalue)
        k=str(k)  
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    a = path+" "+nf_path+"/Data/scpsednc_SPLIT.py "+"-i "+sequence+" -w "+w+" -s "+s+" -k "+k+" -lm "+lm+" -o "+out+" -p"
    for i in prop:
        i=i.lower()
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)

if feature=='BP_DP':
    file = open(out,'w')
    file.close()
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    if args.order == None:
        order = str(1)
    else:
        order = int(args.order)
        order=str(order)
    a = path+" "+nf_path+"/Data/dinucleotide_prop.py "+"-i "+sequence+" -or "+order+" -o "+out+" -p"
    for i in prop:
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)
if feature=='BP_DP_NT':
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    if args.nvalue == None:
        n = str(2)
    else:
        n = str(args.nvalue)
    if args.order == None:
        order = str(1)
    else:
        order = int(args.order)
        order=str(order)
    a = path+" "+nf_path+"/Data/dinucleotide_prop.py_NT "+"-i "+sequence+" -n "+n+" -or "+order+" -o "+out+" -p"
    for i in prop:
        j='"'+i+'"'
        a=a+" "+j
    os.system(a) 
if feature=='BP_DP_CT':
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    if args.cvalue == None:
        m = str(2)
    else:
        m = str(args.cvalue)
    if args.order == None:
        order = str(1)
    else:
        order = int(args.order)
        order=str(order)
    a = path+" "+nf_path+"/Data/dinucleotide_prop_CT.py "+"-i "+sequence+" -c "+m+" -or "+order+" -o "+out+" -p"
    for i in prop:
        j='"'+i+'"'
        a=a+" "+j
    os.system(a) 
if feature=='BP_DP_REST':
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    if args.nvalue == None:
        n = str(0)
    else:
        n = str(args.nvalue)
    if args.cvalue == None:
        m = str(0)
    else:
        m = str(args.cvalue)
    if args.order == None:
        order = str(1)
    else:
        order = int(args.order)
        order=str(order)
    a = path+" "+nf_path+"/Data/dinucleotide_prop_REST.py "+"-i "+sequence+" -n "+n+" -c "+m+" -or "+order+" -o "+out+" -p"
    for i in prop:
        j='"'+i+'"'
        a=a+" "+j
    os.system(a) 
if feature=='BP_DP_SPLIT':
    if(args.property==None):
        print("Invalid number of Arguments.Enter property name in the format -p propertyname")
        exit()
    else:
        prop=args.property
    if args.split == None:
        s = str(1)
    else:
        s = str(args.split)
    if args.order == None:
        order = str(1)
    else:
        order = int(args.order)
        order=str(order)
    a = path+" "+nf_path+"/Data/dinucleotide_prop_SPLIT.py "+"-i "+sequence+" -s "+s+" -or "+order+" -o "+out+" -p"
    for i in prop:
        j='"'+i+'"'
        a=a+" "+j
    os.system(a)


if feature=='NRI':
    file = open(out,'w')
    file.close()
    a = path+" "+nf_path+"/Data/NRI.py "+"-i "+sequence+" -o "+out
    os.system(a)
if feature=='NRI_NT':
    if args.nvalue == None:
        n = str(len(sequence))
    else:
        n = str(args.nvalue)
    a = path+" "+nf_path+"/Data/NRI_NT.py "+"-i "+sequence+" -n "+n+" -o "+out
    os.system(a)
if feature=='NRI_CT':
    if args.cvalue == None:
        n = str(len(sequence))
    else:
        n = str(args.cvalue)
    a = path+" "+nf_path+"/Data/NRI_CT.py "+"-i "+sequence+" -c "+n+" -o "+out
    os.system(a)
if feature=='NRI_REST':
    if args.nvalue == None:
        n = str(0)
    else:
        n = str(args.nvalue)
    if args.cvalue == None:
        m = str(0)
    else:
        m = str(args.cvalue)
    a = path+" "+nf_path+"/Data/NRI_REST.py "+"-i "+sequence+" -n "+n+" -c "+m+" -o "+out
    os.system(a)
if feature=='NRI_SPLIT':
    if args.split==None:
        s=str(1)
    else:
        s=str(args.split)
    a = path+" "+nf_path+"/Data/NRI_SPLIT.py "+"-i "+sequence+" -s "+s+" -o "+out
    os.system(a)
if feature=='DDN':
    file = open(out,'w')
    file.close()
    a = path+" "+nf_path+"/Data/DDON.py "+"-i "+sequence+" -o "+out
    os.system(a)
if feature=='DDN_NT':
    if args.nvalue == None:
        n = str(len(sequence))
    else:
        n = str(args.nvalue)
    a = path+" "+nf_path+"/Data/DDON_NT.py "+"-i "+sequence+" -n "+n+" -o "+out
    os.system(a)
if feature=='DDN_CT':
    if args.cvalue == None:
        n = str(len(sequence))
    else:
        n = str(args.cvalue)
    a = path+" "+nf_path+"/Data/DDON_CT.py "+"-i "+sequence+" -c "+n+" -o "+out
    os.system(a)
if feature=='DDN_REST':
    if args.nvalue == None:
        n = str(0)
    else:
        n = str(args.nvalue)
    if args.cvalue == None:
        m = str(0)
    else:
        m = str(args.cvalue)
    a = path+" "+nf_path+"/Data/DDON_REST.py "+"-i "+sequence+" -n "+n+" -c "+m+" -o "+out
    os.system(a)
if feature=='DDN_SPLIT':
    if args.split==None:
        s=str(1)
    else:
        s=str(args.split)
    a = path+" "+nf_path+"/Data/DDON_SPLIT.py "+"-i "+sequence+" -s "+s+" -o "+out
    os.system(a)
if feature=='ES':
    file = open(out,'w')
    file.close()
    a = path+" "+nf_path+"/Data/ENT.py "+"-i "+sequence+" -o "+out
    os.system(a)
if feature=='ES_NT':
    if args.nvalue == None:
        n = str(len(sequence))
    else:
        n = str(args.nvalue)
    a = path+" "+nf_path+"/Data/ENT_NT.py "+"-i "+sequence+" -n "+n+" -o "+out
    os.system(a)
if feature=='ES_CT':
    if args.cvalue == None:
        n = str(len(sequence))
    else:
        n = str(args.cvalue)
    a = path+" "+nf_path+"/Data/ENT_CT.py "+"-i "+sequence+" -c "+n+" -o "+out
    os.system(a)
if feature=='ES_REST':
    if args.nvalue == None:
        n = str(0)
    else:
        n = str(args.nvalue)
    if args.cvalue == None:
        m = str(0)
    else:
        m = str(args.cvalue)
    a = path+" "+nf_path+"/Data/ENT_REST.py "+"-i "+sequence+" -n "+n+" -c "+m+" -o "+out
    os.system(a)
if feature=='ES_SPLIT':
    if args.split==None:
        s=str(1)
    else:
        s=str(args.split)
    a = path+" "+nf_path+"/Data/ENT_SPLIT.py "+"-i "+sequence+" -s "+s+" -o "+out
    os.system(a)
if feature=='EN':
    file = open(out,'w')
    file.close()
    a = path+" "+nf_path+"/Data/ENT_NL.py "+"-i "+sequence+" -o "+out
    os.system(a)
if feature=='EN_NT':
    if args.nvalue == None:
        n = str(len(sequence))
    else:
        n = str(args.nvalue)
    a = path+" "+nf_path+"/Data/ENT_NL_NT.py "+"-i "+sequence+" -n "+n+" -o "+out
    os.system(a)
if feature=='EN_CT':
    if args.cvalue == None:
        n = str(len(sequence))
    else:
        n = str(args.cvalue)
    a = path+" "+nf_path+"/Data/ENT_NL_CT.py "+"-i "+sequence+" -c "+n+" -o "+out
    os.system(a)
if feature=='EN_REST':
    if args.nvalue == None:
        n = str(0)
    else:
        n = str(args.nvalue)
    if args.cvalue == None:
        m = str(0)
    else:
        m = str(args.cvalue)
    a = path+" "+nf_path+"/Data/ENT_NL_REST.py "+"-i "+sequence+" -n "+n+" -c "+m+" -o "+out
    os.system(a)
if feature=='EN_SPLIT':
    if args.split==None:
        s=str(1)
    else:
        s=str(args.split)
    a = path+" "+nf_path+"/Data/ENT_NL_SPLIT.py "+"-i "+sequence+" -s "+s+" -o "+out
    os.system(a)
    
    
