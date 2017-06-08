#include <iostream>
#include <fstream>
#include "../kmc_api/kmc_file.h"

/**
 * A kmer query engine designed for KMC outpout using kmc_api
 *
 * Usage: query [input database name (w/o) extension] [input queries file] [output check number file]
 *
 * @author: Zeyu Li (zyli@cs.ucla.edu) Jun-5-2017
 */
 
int main(int argc, char* argv[]){
    
    CKMCFile kmer_database;
    std::string input_db;
    std::string input_query_file;
    std::string output_checknum_file;
    
    //-----------------------------------------
    //Parse input parameters
    //-----------------------------------------
    if (argc < 4)
    {
        std::cout<< "Usage:\n\t" << argv[0] << 
            " [input db name] [input queries file] [output check num file]" << std::endl;
        return EXIT_FAILURE;
    }

    input_db = std::string(argv[1]);
    input_query_file = std::string(argv[2]);
    output_checknum_file = std::string(argv[3]);
    
    //----------------------------------------
    //Open kmer database for listing and print kmers within min_count and max_count
    //----------------------------------------

    std::cout << "\tLoading Database \"" << input_db << "\" ..." << std::endl;
    if(! kmer_database.OpenForRA(input_db))
    {
        std::cout << "Cannot run OpenForRA" << std::endl;
        return EXIT_FAILURE;
    }
    else
    {
        std::cout << "\tDatabase load completed!" << std::endl;
        // Several variables that would be used
        uint32 _kmer_length, _mode, _counter_size, _lut_prefix_length, _signature_len, _min_count;
        uint64 _max_count, _total_kmers;

        // Get the info of the database
        kmer_database.Info(_kmer_length, _mode, _counter_size, _lut_prefix_length, _signature_len, _min_count,
                _max_count, _total_kmers);

        // Open input kmer query file and output file
        std::ifstream input_query(input_query_file);
        if(input_query.fail())
        {
            std::cout << "Cannot open file " << input_query_file << " !" << std::endl;
            return EXIT_FAILURE;
        }

        std::ofstream output_num(output_checknum_file);
        if(output_num.fail())
        {
            std::cout << "Cannot open file "<< output_checknum_file << " !" << std::endl;
            return EXIT_FAILURE;
        }


        // Read each line and query in the database
        std::cout << "\tReading k-mers and doing queries ... " << std::endl;
        for( std::string query; getline( input_query, query ); )
        {
            uint32 kmer_count = 0;
            // Declare a KmerAPI object used for kmer query
            CKmerAPI kmer_object(_kmer_length);
            std::string query_trim = query.substr(0, query.size() -1);
            kmer_object.from_string(query_trim);
            if(! (kmer_database.CheckKmer(kmer_object, kmer_count)))
                output_num << "0\n";
            else
                output_num << kmer_count << "\n";
        }
        std::cout << "\tQueries finished. The please check " << output_checknum_file << " for results." << std::endl;
        kmer_database.Close();
    }
    return EXIT_SUCCESS;
}



