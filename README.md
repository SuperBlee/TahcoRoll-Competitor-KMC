Kmer Query based on KMC
==================================

### 1. What's inside.
    .
    ├── bin
    │   ├── kmc
    │   ├── kmcV1
    │   ├── kmcV22
    |   ├── kmc_dump
    │   └── query
    ├── kmer_query.py
    ├── api_call_query.cpp
    └── run.sh

You can see above files in this repository.
`bin` includes three version of kmc's and and api program that is executable. Try `./bin/query` to see the short usage.`kmc` is the 3.0.0 version, `kmcV1` is the 1.0.0 version, `kmcV22` is the 2.2.0 version, `kmc_dump` is the tools for dumping the all the kmer counts. Try `./bin/kmc`, `./bin/kmcV1`, `./bin/kmcV22` to see the usage of the kmc's, and `./bin/kmc_dump` to see the how to dump the kmers.

### 1.5 What do you input?
3 parameters.
- (1) input fastq file.
- (2) input the file that contains the query batch. It doesn't have to be sorted by length.
- (3) input the name of the output kmer count files that you like.

### 2. How about the query?
All the database constructing and query doing works are in kmer_query.py. I think I add enough comments so that you can understand the mechanism of it. Try python3 kmer_query.py to see the usage. You can also check the very short `run.sh` as an example of how to give the arguments. (In the interest of space, I had all the ../data/ dir removed, you can put all your data there if you wish.)

### 3. How to change the version?
In `kmer_query.py`, change __line 84__ where ```subprocess.call([KMC_PATH_3, ...```, just change `KMC_PATH_3` to `KMC_PATH_2` or `KMC_PARH_1` as you like.

### 4. How to do the timing?
I didn't do that for now. I got to finish my final project reports. sorry. But I think that's not hard.

### 5. What's next?
- Put the selection of kmc versions into arguments.
- Include the API call code
- Implement automatic timers
- ... (Any other stuff that looks cool but I am not going to do for sure.)

Have fun!

-- Z

#### New
Now the output of the `query` for a single string _s_ is the summation of the count of _s_ and its complement stirng.
