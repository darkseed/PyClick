import codecs
import argparse

__author__ = 'Zhuyun Dai'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("org_sessions_filename")
    parser.add_argument("query_freq_filename")
    parser.add_argument("query_freq_cutoff", type=int, help="only select sessions with q"
                                                            "uery appearing more than the cutoff")
    parser.add_argument("output_filename")
    args = parser.parse_args()

    # read frequent queries
    query_freq_file = codecs.open(args.query_freq_filename, 'r', 'euc-cn', errors='replace')
    selected_queries = set()
    for line in query_freq_file:
        entry_array = line.strip().split("\t")
        freq = int(entry_array[0])
        query = entry_array[1].strip()
        if freq < args.query_freq_cutoff:
            break
        selected_queries.add(query)
    
    print "selecting {0} queries".format(len(selected_queries))

    # filter session_file
    sessions_file = codecs.open(args.org_sessions_filename, 'r', 'euc-cn', errors='replace')
    output_file = codecs.open(args.output_filename, 'w', 'euc-cn', errors='replace')
    for line in sessions_file:
        entry_array = line.strip().split("\t")
        query = entry_array[1].strip()
        if query in selected_queries:
            output_file.write(line)

    query_freq_file.close()
    sessions_file.close()
    output_file.close()


if __name__ == '__main__':
    main()
