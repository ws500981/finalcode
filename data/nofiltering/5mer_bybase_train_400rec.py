from __future__ import print_function
from Bio import SeqIO
import Bio
import csv
with open("SRR10971019_subreads.fastq") as handle:
    records = list(SeqIO.parse(handle, "fastq"))

#USED, CAN GET CORRECT RESULT, sliding window by base
import sys
with open("train_bybase.tsv", "w", newline = '') as f:
    for i in range(0, 400): #int(records[-1].id[12:])): 
        first_record = records[i] # REMEMBER TO CHANGE THIS BACK TO i
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
            print(len(element))
            sentence = ""
            base = 0
            while base<=65:
                if base == 0:
                    tempList = []
                    for q in range(0,5):
                        tempList.append(element[q])
                    word = separator.join(tempList)
                    #print(word, base, sentence)
                    base = 1
                    sentence = word
                elif base==65:
                    tempList = []
                    for q in range(0,5):
                        tempList.append(element[base+q])
                    word = separator.join(tempList)
                    #print(word, base, sentence)
                    base += 1
                    sentence = sentence + "\t" + word
                else:
                    tempList = []
                    for q in range(0,5):
                        tempList.append(element[base+q])
                    word = separator.join(tempList)
                    #print(word, base, sentence)
                    base += 1
                    sentence = sentence + " " + word
            print("%s" % (sentence), file=f)
            #print(sentence)