import argparse
import json
import sys
reload(sys)
sys.setdefaultencoding('UTF8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("qid2query_file")
    parser.add_argument("click_model_file")
    parser.add_argument("session_file")
    parser.add_argument("output_file", type=argparse.FileType('w'))
    args = parser.parse_args()

    # read selected queries
    query2qid = {}
    for line in open(args.qid2query_file, 'r'):
        qid, query = line.strip().split('\t')
        query2qid[query] = int(qid)

    # read session file
    pid2doc = {}
    for line in open(args.session_file, 'r'):
        line = line.strip()
        obj = json.loads(line)
        for doc in obj['documents']:
            pid = doc['id']
            pid2doc[pid] = doc

    # read click model file
    prev_qid = -1
    rank = 0
    for line in open(args.click_model_file, 'r'):
        items = line.strip().split()
        query = ' '.join(items[0:-2])
        pid = items[-2]
        score = items[-1]
        qid = query2qid[query]
        if qid != prev_qid:
            prev_qid = qid
            rank = 0
        rank += 1
        doc = pid2doc[pid]
        obj = {"query": query, "doc": doc}
        jstr = json.dumps(obj)
        args.output_file.write("{0}\tQ0\t{1}\t{2}\t{3} # {4}\n".format(qid, pid, rank, score, jstr))
