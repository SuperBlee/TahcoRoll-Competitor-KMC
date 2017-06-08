#!/usr/bin/env python3

import sys, os
import subprocess
import shutil

"""
===================
KMC Kmer Query
===================

Workflow:
    1. Read test files. Sort by length. Output to files.
    2. For each length of k-mer k, load fastq files, construct databases, query on this db.

@author: Zeyu Li zyli@cs.ucla.edu
"""

if __name__ == "__main__":
    # Check if arguments are valid
    # arguments format: python3 kmer_query.py <input fq file name> <query batch file name>
    if len(sys.argv) < 1 + 3:
        print("--Usage python3 %s <input fastq file> <query batch file> <output file name>" % sys.argv[0], file=sys.stderr)
        sys.exit()

    # set dir of the bin files
    KMC_PATH_3 = "./bin/kmc"  # the path of KMC version 3.0.0
    KMC_PARH_1 = "./bin/kmcV1"  # the path of KMC version 1.0.0
    KMC_PARH_2 = "./bin/kmcV22"  # the path of KMC version 2.2.0
    QUERY_PATH = "./bin/query"

    # set dir of the temporary files
    QRY_DIR = "./qry/"  # dir to store the partitioned query files sorted by length
    DB_DIR = "./db/"  # dir to store the kmer-database created by KMC
    OUT_DIR = "./out/"  # dir to store the output files

    # load input fastq file name and query batch file
    fq_path = sys.argv[1]
    fq_name = os.path.splitext(os.path.basename(fq_path))[0]  # extract file name w/o extension
    qb_path = sys.argv[2]
    qb_name = os.path.splitext(os.path.basename(qb_path))[0]  # extract file name w/o extension
    out_name = sys.argv[3]

    # load the batch file to memory
    kmer_partition = {}
    print("Loading the query batch file into mem ...")
    with open(qb_path, "r") as fin:
        for kmer in fin:
            len_kmer = len(kmer.strip())
            if len_kmer not in kmer_partition:
                kmer_partition[len_kmer] = [kmer.strip()]
            else:
                kmer_partition[len_kmer].append(kmer.strip())

    # make a directory to store all sorted and partitioned files
    if not os.path.exists(QRY_DIR):
        os.makedirs(QRY_DIR)

    # Output the file name as qry_batch+length.txt name
    print("Outputting the files sorted by length to disk ... ")
    for length, kmer_list in kmer_partition.items():
        with open(QRY_DIR + qb_name + "_" + str(length) + ".txt", "w") as fout:
            for kmer in kmer_list:
                print(kmer, file=fout)

    # make directory for the storage of kmer-databases
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    # make directory for output the files
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    print("\n=========================\nStart K-mer queries.\n=========================\n")

    # For different lengths, load databases and the do the query
    kmer_lens = list(kmer_partition.keys())
    for kmer_len in kmer_lens:
        print("\nConstructing the database of len " + str(kmer_len))
        # cmd: ../KMC/bin/kmc [fq_name] ./db/[fq_label]_[str(len)] ./db/
        subprocess.call([KMC_PATH_3, "-k"+str(kmer_len), fq_path, DB_DIR + fq_name + "_" + str(kmer_len), DB_DIR])
        print("Completed constructing the database.\n")
        # give the cmd: ../KMC/bin/query ./db/[fq_label}_[str(kmer_len)] ./tmp/
        subprocess.call([QUERY_PATH, DB_DIR + fq_name + "_" + str(kmer_len),
                         QRY_DIR + qb_name + "_" + str(kmer_len) + ".txt", OUT_DIR + out_name + "_" + str(kmer_len) + ".txt"])

    # remove the temporary directories: ./qry/ and ./db/
    print("Removing the temporary directories.")
    shutil.rmtree(QRY_DIR)
    shutil.rmtree(DB_DIR)


