#!/usr/bin/python

#########################################################################
### De novo pipeline for processing READ 1 only -- PILOT LIBRARY TEST ###
#########################################################################

from integrated_denovo_pipeline import *
from DBR_Parsing import *
from assembled_DBR_filtering import *

# PATHS TO INPUTS AND OUTPUTS
# user only needs to specify parent directory; the remaining directories should be automatically generated

## For initial assembly and DBR filtering
parentDir = '/home/pierce/CWD_RADseq/raw/'
pearInDir = parentDir
pearOutDir = parentDir + '/pear_merged_parallel/'
filterInDir = pearOutDir
filterOutDir =  parentDir + '/qual_filtered/'
dbrInDir = filterOutDir
dbrOutDir = parentDir + '/DBR_dir/'
demultiplexInDir = filterOutDir
demultiplexOutDir = parentDir + '/demultiplexed/'
trimInDir = demultiplexOutDir
trimOutDir = parentDir + '/trimmed/'
stacksInDir = trimOutDir
stacksOutDir = parentDir + '/StacksOutput/' # stacks doesn't allow an output to be specified
pseudorefInDir = stacksOutDir
pseudorefOutDir = parentDir + '/pseudoreference.fastq'
BWAinDir = parentDir
BWAoutDir = parentDir + '/BWA/'
DBRfilteredseqs = parentDir + '/dbrFiltered/'

# ASSEMBLE ITERATIVELY WITH PEAR 
out_name = 'pear_merged_'
extra_params = '-m 309 -n 209'
#iterative_PEAR_assemble(in_dir = pearInDir, 
#                        out_dir = pearOutDir, 
#                        out_name = out_name, 
#                        extra_params = extra_params,
#                        regexR1='R1', regexR2='R2')

# QUALITY FILTER PEAR ASSEMBLED DATA
out_name = '.qual_filtered' # gets appended to input file name
q = 30
p = 50
read = '.assembled.fastq' # extension for pear-assembled reads
#iterative_FASTQ_quality_filter(directory = filterInDir, 
#                               out_dir = filterOutDir, 
#                               out_name = out_name, 
#                               q = q, 
#                               p = p, 
#                               read = read)

# MAKE DBR DICTIONARIES FOR QUAL FILTERED PEAR DATA
seq_type = 'pear'
#iterative_DBR_dict(in_dir = dbrInDir, 
#                   seqType = seq_type,
#                   save = dbrOutDir,
#                   dbr_start = -10,
#                   dbr_stop = -2)

# DEMULTIPLEX
out_prefix = '/demultiplexed_'
#iterative_Demultiplex(in_dir = demultiplexInDir, 
#                      barcode_dir = '/home/pierce/CSU_ChronicWasting/BarcodesRound1/', 
#                      out_dir = demultiplexOutDir, 
#                      out_prefix = out_prefix)

# TRIM TO UNIFORM LENGTH
suffix = '_trimmed.fq'
first_base = 11
last_base = 196
#Trim(in_dir = trimInDir, 
#     out_dir = trimOutDir, 
#     suffix = suffix, 
#     first_base = first_base, 
#     last_base = last_base)

# RUN STACKS SIMULTANEOUSLY ON ALL LIBRARIES
#denovo_Stacks(in_dir = stacksInDir, 
#              denovo_path = denovo_path, 
#              stacks_executables = stacks_executables, 
#              out_dir = stacksOutDir, 
#              m = 10, 
#              n = 2, 
#              b = 1, 
#              D = '_initial_assembly')

# GENERATE THE PSEUDOREFERENCE GENOME
#GeneratePseudoref(in_dir = pseudorefInDir, 
#                  out_file = pseudorefOutDir,  
#                  BWA_path = BWA) # imported from integrated_denovo_pipeline.py

# REFERENCE MAP QUALITY FILTERED/DEMULTIPLEXED MERGED READS TO THE PSEUDOREFERENCE
#refmap_BWA(in_dir = trimOutDir, # input demultiplexed, trimmed reads
#           out_dir = BWAoutDir, 
#           BWA_path = BWA, # imported from integrated_denovo_pipeline.py 
#           pseudoref_full_path = pseudorefOutDir)


#DBR_Filter(assembled_dir = BWAoutDir, # the SAM files for the data mapped to pseudoreference
#           out_dir = DBRfilteredseqs, # the output file, full path, ending with .fasta
#           n_expected = 2, # the number of differences to be tolerated
#           barcode_dir = '/home/pierce/CSU_ChronicWasting/BarcodesRound1/', # the barcodes for individuals in the library referenced in dict_in
#           dict_dir = dbrOutDir, # a single dictionary of DBRs (for one library only)
#           barcode_file=None, # if just a single library is being used, can directly pass the barcode file
#           test_dict=True, # optionally print testing info to stdout for checking the dictionary construction
#           phred_dict=phred_dict, # dictionary containing ASCII quality filter scores to help with tie breaks
#           samMapLen=None)


### Part 2: Re-assembling the filtered sequences

## For final assembly post DBR filtering
re_demultiplexInDir = DBRfilteredseqs
re_demultiplexOutDir = parentDir + '/dbrFiltered_demultiplexed/'
re_trimInDir = re_demultiplexOutDir
re_trimOutDir = parentDir + '/dbrFiltered_trimmed/'
re_stacksInDir = re_trimOutDir
re_stacksOutDir = parentDir + '/dbrFiltered_StacksOutput/' # stacks doesn't allow an output to be specified
re_pseudorefInDir = re_stacksOutDir
re_pseudorefOutDir = parentDir + '/dbrFiltered_pseudoreference.fastq'
re_BWAinDir = parentDir
re_BWAoutDir = parentDir + '/dbrFiltered_BWA2/'
finalBCFout = parentDir + '/dbrFiltered_pseudorefMapped_genotypes2.bcf'
finalVCFout = parentDir + '/dbrFiltered_pseudorefMapped_genotypes2.vcf'

# DEMULTIPLEX
#out_prefix = '/re_demultiplexed_'
#iterative_Demultiplex(in_dir = re_demultiplexInDir, 
#                      barcode_dir = '/home/pierce/CSU_ChronicWasting/BarcodesRound1/', 
#                      out_dir = re_demultiplexOutDir, 
#                      out_prefix = out_prefix)

# TRIM TO UNIFORM LENGTH
#suffix = '_re_trimmed.fq'
### what are the new first and last bases??? we should just be removing the barcode we added back after DBR filtering... enzyme cut sites & DBRs should be gone
#new_first_base = 6
#Trim(in_dir = re_trimInDir, 
#     out_dir = re_trimOutDir, 
#     suffix = suffix, 
#     first_base = new_first_base)

## no real need to re-run stacks and re-generate a pseudoreference.
## samtools mpileup can enforce a depth threshold for SNP calls, so stacks that wouldn't have been made
## with filtered data will not produce SNPs.

# RUN STACKS SIMULTANEOUSLY ON ALL LIBRARIES
denovo_Stacks(in_dir = re_stacksInDir, 
              denovo_path = denovo_path, 
              stacks_executables = stacks_executables, 
              out_dir = re_stacksOutDir, 
              m = 10, 
              n = 2, 
              b = 1, 
              D = '_final_assembly')

# GENERATE THE PSEUDOREFERENCE GENOME
GeneratePseudoref(in_dir = re_pseudorefInDir, 
                  out_file = re_pseudorefOutDir,  
                  BWA_path = BWA) # imported from integrated_denovo_pipeline.py

# REFERENCE MAP QUALITY FILTERED/DEMULTIPLEXED MERGED READS TO THE PSEUDOREFERENCE
refmap_BWA(in_dir = re_trimOutDir, # input demultiplexed, trimmed reads
           out_dir = re_BWAoutDir, 
           BWA_path = BWA, # imported from integrated_denovo_pipeline.py 
           pseudoref_full_path = re_pseudorefOutDir)

# CALL THE GENOTYPES USING SAMTOOLS MPILEUP; CONVERT OUTPUT TO VCF FILE
callGeno(sam_in = re_BWAoutDir, 
         pseudoref = re_pseudorefOutDir, 
         BCFout = finalBCFout, 
         VCFout = finalVCFout)
