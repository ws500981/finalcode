from __future__ import print_function

import csv
import logging
import sys

import Bio
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

logger = logging.getLogger(__name__)
from pafpy import PafFile

path = "trimmed_mapping.paf"

#read the mapping result .paf file and save the ids of those with matching bases 
identities = []
with PafFile(path) as paf:
    for record in paf:
        #set no. of matching bases / query length to be 0.9
        if (record[9]/record[1]) > 0.9:
            identities.append(record[0][12:])

#train test split 7:3
train = int(len(identities)*0.7)
dev = len(identities) - train
print("train: ", train, "dev: ", dev)

with open("SRR10971019_subreads.fastq") as handle:
    records = list(SeqIO.parse(handle, "fastq"))

#prepare dataset from with sliding window by base method
with open("filtered_0.9_train_bybase_3mer.tsv", "w", newline = '') as f:
    for a in range(0,train):
        i = int(identities[a]) 
        first_record = records[i]
        strrep = str(first_record.seq)
        print("STRREP", len(strrep))

        strrep = strrep[:len(strrep)-len(strrep)%70]
        n = 0
        while n<=len(strrep) and len(strrep)-n>71:
            if n == 0:
                n = 70
                strrep = strrep[:n] + "\t" + strrep[n:]

            else:
                n = n + 71
                strrep = strrep[:n] + "\t" + strrep[n:]

        print("after adding tabs: ", len(strrep))
        arr = strrep.split("\t")


        separator = ''
        for element in arr:
            sentence = ""
            base = 0
            while base<=67:
                if base == 0:
                    tempList = []
                    for q in range(0,3):
                        tempList.append(element[q])
                    word = separator.join(tempList)
                    base = 1
                    sentence = word
                elif base==67:
                    tempList = []
                    for q in range(0,3):
                        tempList.append(element[base+q])
                    word = separator.join(tempList)
                    base += 1
                    sentence = sentence + "\t" + word
                else:
                    tempList = []
                    for q in range(0,3):
                        tempList.append(element[base+q])
                    word = separator.join(tempList)
                    base += 1
                    sentence = sentence + " " + word
            print("%s" % (sentence), file=f)

with open("filtered_0.9_dev_bybase_3mer.tsv", "w", newline = '') as f:
    for b in range(train, len(identities)):
        i = int(identities[b]) 
        first_record = records[i]
        strrep = str(first_record.seq)
        print("STRREP", len(strrep))

        strrep = strrep[:len(strrep)-len(strrep)%70]
        n = 0
        while n<=len(strrep) and len(strrep)-n>71:
            if n == 0:
                n = 70
                strrep = strrep[:n] + "\t" + strrep[n:]

            else:
                n = n + 71
                strrep = strrep[:n] + "\t" + strrep[n:]

        print("after adding tabs: ", len(strrep))
        arr = strrep.split("\t")

        separator = ''
        for element in arr:
            sentence = ""
            base = 0
            while base<=67:
                if base == 0:
                    tempList = []
                    for q in range(0,3):
                        tempList.append(element[q])
                    word = separator.join(tempList)
                    base = 1
                    sentence = word
                elif base==67:
                    tempList = []
                    for q in range(0,3):
                        tempList.append(element[base+q])
                    word = separator.join(tempList)
                    base += 1
                    sentence = sentence + "\t" + word
                else:
                    tempList = []
                    for q in range(0,3):
                        tempList.append(element[base+q])
                    word = separator.join(tempList)
                    base += 1
                    sentence = sentence + " " + word
            print("%s" % (sentence), file=f)
