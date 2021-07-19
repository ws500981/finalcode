from __future__ import print_function
from Bio import SeqIO
import Bio
from Bio.SeqRecord import SeqRecord
import csv
import logging
logger = logging.getLogger(__name__)
from pafpy import PafFile
#path = "mapping.paf"
path = "trimmed_mapping.paf"

#read the mapping result file and save the ids of those with matching bases 
identities = []
#i = 0 # the i is for debugging purposes
with PafFile(path) as paf:
    for record in paf:
        #print("query length: ", record[1])
        #print("query start coor: ", record[2])
        #print("query end coor: ", record[3])
        #print("query_end - query_start: ", record[3]-record[2]) # != record[10] bc there might be addition/deletion/substitution
        #print("no of matching bases: ", record[9])
        ##print("no of matching bases with gaps: ", record[10])
        ##print("query matching length: ", record[3]-record[2])
        ##print("target matching length: ", record[8]-record[7])
        #print("(query_end - query_start) / query length: ", (record[3]-record[2])/record[1])
        #print("no of matching bases / query_length: ", record[9]/record[1])
        #print("\n")
        if (record[9]/record[1]) > 0.9:
            identities.append(record[0][12:])
        
    # the i is for debugging purposes
        #i+=1
        #if i == 60:
        #    break

train = int(len(identities)*0.7)
dev = len(identities) - train
print("train: ", train, "dev: ", dev)

with open("SRR10971019_subreads.fastq") as handle:
    records = list(SeqIO.parse(handle, "fastq"))

#USED, CAN GET CORRECT RESULT, sliding window by base
import sys
with open("filtered_0.9_train_bybase_3mer.tsv", "w", newline = '') as f:
    for a in range(0,train):
        i = int(identities[a]) 
        first_record = records[i]
        #print(type(first_record.seq)) # type is <class 'Bio.Seq.Seq'>
        strrep = str(first_record.seq)
        print("STRREP", len(strrep)) # type(strrep) = <class 'str'>
        #print(strrep) #print out the sequence

        strrep = strrep[:len(strrep)-len(strrep)%70]
        n = 0
        while n<=len(strrep) and len(strrep)-n>71:
            if n == 0:
                n = 70
                strrep = strrep[:n] + "\t" + strrep[n:]
                #print("n=",n)
            else:
                n = n + 71
                strrep = strrep[:n] + "\t" + strrep[n:]
                #print("n=",n)
        print("after adding tabs: ", len(strrep))
        arr = strrep.split("\t")
        #print(arr)

        separator = ''
        for element in arr:
            #print(len(element))
            sentence = ""
            base = 0
            while base<=67:
                if base == 0:
                    tempList = []
                    for q in range(0,3):
                        tempList.append(element[q])
                    word = separator.join(tempList)
                    #print(word, base, sentence)
                    base = 1
                    sentence = word
                elif base==67:
                    tempList = []
                    for q in range(0,3):
                        tempList.append(element[base+q])
                    word = separator.join(tempList)
                    #print(word, base, sentence)
                    base += 1
                    sentence = sentence + "\t" + word
                else:
                    tempList = []
                    for q in range(0,3):
                        tempList.append(element[base+q])
                    word = separator.join(tempList)
                    #print(word, base, sentence)
                    base += 1
                    sentence = sentence + " " + word
            print("%s" % (sentence), file=f)
            #print(sentence)

with open("filtered_0.9_dev_bybase_3mer.tsv", "w", newline = '') as f:
    for b in range(train, len(identities)):
        i = int(identities[b]) 
        first_record = records[i]
        #print(type(first_record.seq)) # type is <class 'Bio.Seq.Seq'>
        strrep = str(first_record.seq)
        print("STRREP", len(strrep)) # type(strrep) = <class 'str'>
        #print(strrep) #print out the sequence

        strrep = strrep[:len(strrep)-len(strrep)%70]
        n = 0
        while n<=len(strrep) and len(strrep)-n>71:
            if n == 0:
                n = 70
                strrep = strrep[:n] + "\t" + strrep[n:]
                #print("n=",n)
            else:
                n = n + 71
                strrep = strrep[:n] + "\t" + strrep[n:]
                #print("n=",n)
        print("after adding tabs: ", len(strrep))
        arr = strrep.split("\t")
        #print(arr)

        separator = ''
        for element in arr:
            #print(len(element))
            sentence = ""
            base = 0
            while base<=67:
                if base == 0:
                    tempList = []
                    for q in range(0,3):
                        tempList.append(element[q])
                    word = separator.join(tempList)
                    #print(word, base, sentence)
                    base = 1
                    sentence = word
                elif base==67:
                    tempList = []
                    for q in range(0,3):
                        tempList.append(element[base+q])
                    word = separator.join(tempList)
                    #print(word, base, sentence)
                    base += 1
                    sentence = sentence + "\t" + word
                else:
                    tempList = []
                    for q in range(0,3):
                        tempList.append(element[base+q])
                    word = separator.join(tempList)
                    #print(word, base, sentence)
                    base += 1
                    sentence = sentence + " " + word
            print("%s" % (sentence), file=f)
            #print(sentence)
