import codecs
import argparse

__author__ = 'Zhuyun Dai'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("org_sessions_filename")
    parser.add_argument("query_filename")
    parser.add_argument("output_filename")
    args = parser.parse_args()

    # read frequent queries
    query_file = codecs.open(args.query_filename, 'r', 'utf-8', errors='replace')
    selected_queries = {} 
    for line in query_file:
        entry_array = line.strip().split("\t")
        qid = int(entry_array[0])
        query = entry_array[1].strip()
        selected_queries[query] = qid
    
    print "selecting {0} queries".format(len(selected_queries))

    # filter session_file
    sessions_file = codecs.open(args.org_sessions_filename, 'r', 'utf-8', errors='replace')
    output_file = codecs.open(args.output_filename, 'w', 'utf-8', errors='replace')
    for line in sessions_file:
        entry_array = line.strip().split("\t")
        if len(entry_array) < 2: continue
        query = entry_array[1].strip()
        if query in selected_queries:
            output_file.write(line)

    query_file.close()
    sessions_file.close()
    output_file.close()


if __name__ == '__main__':
    main()
