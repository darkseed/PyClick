import argparse
import sys
reload(sys)
sys.setdefaultencoding('UTF8')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query_log_file", type=argparse.FileType('r'))
    parser.add_argument("qid2query_file", type=argparse.FileType('r'))
    parser.add_argument("url2docid_file", type=argparse.FileType('r'))
    parser.add_argument("output_file", type=argparse.FileType('w'))
    args = parser.parse_args()

    # read queries
    queries = {}
    for line in args.qid2query_file:
        qid, query = line.strip().split('\t')
        query = query.replace(' ', '')
        queries[query] = qid
        print query
    visited = set()

    # read url2docid
    url2docid = {}
    for line in args.url2docid_file:
        docid, url = line.strip().split('\t')
        url2docid[url] = docid

    # read and filter search log
    n_lines = 0
    for line in args.query_log_file:
        n_lines += 1
        if n_lines % 10000 == 0:
            print n_lines
            print len(visited)
        if len(visited) == len(queries):
            break
        entry_array = line.strip().split("\t")

        if len(entry_array) % 4 != 2:  # format checking
            #print line
            continue

        usr_id, session_id, begin_time = entry_array[0].split('#')
        query = entry_array[1].strip().replace(' ', '')

        if query not in queries:
            continue
        qid = queries[query]
        if qid in visited:
            continue
        visited.add(qid)
        print qid

        i = 2
        rank = 0

        while i < len(entry_array):
            url, if_click = entry_array[i: i + 2]
            #assert (url in url2docid), url
            if url not in url2docid:
                i += 4
                print url
                continue
            docid = url2docid[url]
            i += 4
            rank += 1

            outstr = "{0} 0 {1} {2} {3} # sogou-org-ranking\n".format(qid, docid, rank, -rank)
            args.output_file.write(outstr)



