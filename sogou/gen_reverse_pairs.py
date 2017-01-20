import sys
reload(sys)
sys.setdefaultencoding('UTF8')

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query_log_file",  type=argparse.FileType('r'))
    parser.add_argument("qid2query_file",  type=argparse.FileType('r'))
    parser.add_argument("url2docid_file", type=argparse.FileType('r'))
    parser.add_argument("output_file", type=argparse.FileType('w'))
    args = parser.parse_args()

    # read queries
    queries = {}
    for line in args.qid2query_file:
        qid, query = line.strip().split('\t')
        queries[query] = qid
    visited = set()

    # read url2docid
    url2docid = {}
    for line in args.ulr2docid_file:
        docid, url = line.strip().split('\t')
        url2docid[url] = docid

    # read and filter search log
    for line in args.query_log_file:
        entry_array = line.strip().split("\t")

        if len(entry_array) % 4 != 2:  # format checking
            continue

        usr_id, session_id, begin_time = entry_array[0].split('#')
        query = entry_array[1].strip()

        if query not in queries:
            continue
        qid = queries[query]

        i = 2
        rank = 0

        not_clicked = []
        while i < len(entry_array):
            url, if_click = entry_array[i: i + 2]
            if url not in url2docid:
                continue
            docid = url2docid[url]

            if_click = int(if_click)

            if if_click == 0:
                not_clicked.append(docid)
            else:
                for neg in not_clicked:
                    args.output_file.write('{0}\t{1}\t{2}\n'.format(qid, docid, neg))
            i += 4





