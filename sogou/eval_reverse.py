import sys
reload(sys)
sys.setdefaultencoding('UTF8')

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("trec_file", type=argparse.FileType('r'))
    parser.add_argument("reversed_click_pair_file", type=argparse.FileType('r'))
    args = parser.parse_args()

    # read trec
    trec = {}
    for line in args.trec_file:
        #  1 Q0 sogou-15630 1 0.601785 # ranklib
        items = line.split()
        qid = int(items[0])
        docid = items[2]
        rank = int(items[3])
        if rank > 10: # only eval top10
            continue
        if qid not in trec:
            trec[qid] = {}
        trec[qid][docid] = rank

    # read reversed pairs
    query_total = [0] * 10001
    query_correct = [0] * 10001

    for line in args.reversed_click_pair_file:
        qid, pos, neg = line.strip().split('\t')
        if qid not in trec:
            continue
        if pos in trec[qid] and neg in trec[qid]:
            rank1 = trec[qid][pos]
            rank2 = trec[qid][neg]
            query_total[qid] += 1.0
            if rank1 < rank2: # correct
                query_correct[qid] += 1.0

    for qid in range(1, 10001):
        if query_total[qid] == 0:
            continue
        print qid, query_correct[qid]/query_total[qid]






