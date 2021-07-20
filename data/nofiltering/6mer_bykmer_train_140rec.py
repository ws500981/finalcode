from __future__ import print_function
from Bio import SeqIO
import Bio
import csv
with open("SRR10971019_subreads.fastq") as handle:
    records = list(SeqIO.parse(handle, "fastq"))

#sliding window by kmers
with open("train_bykmer.tsv", "w", newline = '') as f:
    for i in range(0, 140): 
        first_record = records[i]
        strrep = str(first_record.seq)
        print("STRREP", len(strrep))
        
        strrep = strrep[:len(strrep)-len(strrep)%6]
        n = 0
        while n<=len(strrep) and len(strrep)-n>7:
            if n == 0:
                n = 6
                strrep = strrep[:n] + "\t" + strrep[n:]

            else:
                n = n + 7
                strrep = strrep[:n] + "\t" + strrep[n:]

        print("after adding tabs: ", len(strrep))
        arr = strrep.split("\t")

        tsv_output = csv.writer(f, delimiter=' ')
        flag = True
        for p in range(0,len(arr)+1):
            arr1 = []
            for q in range(0,64):
                try:
                    arr1.append(arr[p+q])
                except:
                    flag = False
            if flag and p+q+1<len(arr):
                arr1[63] = arr1[63] + '\t' + arr[p+q+1]
                tsv_output.writerow(arr1)