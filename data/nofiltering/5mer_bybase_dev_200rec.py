from __future__ import print_function
from Bio import SeqIO
import Bio
import csv
with open("SRR10971019_subreads.fastq") as handle:
    records = list(SeqIO.parse(handle, "fastq"))

#sliding window by base
import sys
with open("dev_bybase.tsv", "w", newline = '') as f:
    for i in range(400, 600):
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
            print(len(element))
            sentence = ""
            base = 0
            while base<=65:
                if base == 0:
                    tempList = []
                    for q in range(0,5):
                        tempList.append(element[q])
                    word = separator.join(tempList)
                    base = 1
                    sentence = word
                elif base==65:
                    tempList = []
                    for q in range(0,5):
                        tempList.append(element[base+q])
                    word = separator.join(tempList)
                    base += 1
                    sentence = sentence + "\t" + word
                else:
                    tempList = []
                    for q in range(0,5):
                        tempList.append(element[base+q])
                    word = separator.join(tempList)
                    base += 1
                    sentence = sentence + " " + word
            print("%s" % (sentence), file=f)