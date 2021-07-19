from __future__ import print_function
from Bio import SeqIO
import Bio
import csv
import logging
#logger = logging.getLogger(__name__)
#logger.info("loading records")
with open("SRR10971019_subreads.fastq") as handle:
    records = list(SeqIO.parse(handle, "fastq"))
#logger.info("finished loading records")

#USED, CAN GET CORRECT RESULT, non-overlapping
#for each record, convert the sequence to string. Method 1 (preferred because there is no title and no ending '\n')
with open("dev_nonoverlapping.tsv", "w", newline = '') as f:
    for i in range(10000, 15000): #int(records[-1].id[12:])): 
        first_record = records[i]
        #print(type(first_record.seq)) # type is <class 'Bio.Seq.Seq'>
        strrep = str(first_record.seq)
        print( len(strrep),"base") # type(strrep) = <class 'str'>
        #print(strrep) #print out the sequence
        
        strrep = strrep[:len(strrep)-len(strrep)%6]
        #logger.info("loading record %d", i)
        #logger.info("record length: %d", len(strrep))
	
        #format1: non-overlapping (if (len_after-remainder)/7 == (len_before-remainder)/6 then the splitting is correct)
        #use the same method to insert '\n' such that each line contains 65 6-mers
        # [TODO] save the string as tsv
        n = 0
        while n<=len(strrep) and len(strrep)-n>7:
            if n == 0:
                n = 6
                strrep = strrep[:n] + "\t" + strrep[n:]
                #print("n=",n)
            else:
                n = n + 7
                strrep = strrep[:n] + "\t" + strrep[n:]
                #print("n=",n)
        print(len(strrep), " \t")

        arr = strrep.split("\t")
        #print(arr)
        tsv_output = csv.writer(f, delimiter=' ')
        flag = True
        for p in range(0,len(arr)+1,65):
            arr1 = []
            for q in range(0,64):
                try:
                    arr1.append(arr[p+q])
                except:
                    flag = False
            if flag and p+q+1<len(arr):
                #print("before: ",arr1[63])
                arr1[63] = arr1[63] + '\t' + arr[p+q+1]
                #print("after: ",arr1[63])
                #print(arr1)
                tsv_output.writerow(arr1)
        #break