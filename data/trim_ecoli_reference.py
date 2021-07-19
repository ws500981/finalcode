from __future__ import print_function
from Bio import SeqIO
import Bio
from Bio.SeqRecord import SeqRecord

with open("escherichia_coli_reference.fasta") as handle:
    reference = list(SeqIO.parse(handle, "fasta"))

print("ori_reference_length: ", len(str(reference[0].seq)))

file_out='trimmed_100000.fasta'
with open(file_out, 'w') as f_out:
    for seq_record in reference:
        print("original sequence record: \n", seq_record)
        print("length of ori-sequence: ", len(str(reference[0].seq)), "\n")
        
        seq_record.seq = seq_record.seq[:100000]
        seq_record.description = seq_record.description.replace("complete genome", "100,000 bases")
        
        print("trimmed sub-sequence record: \n", seq_record)
        r=SeqIO.write(seq_record, f_out, 'fasta')
        if r!=1: print('Error while writing sequence:  ' + seq_record.id)
        print("length of sub-sequence: ", len(str(reference[0].seq)))