import argparse
import sys
import csv
reload(sys)
sys.setdefaultencoding('UTF8')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("in_log_file", type=argparse.FileType('r'))
    parser.add_argument("output_file", type=argparse.FileType('w'))
    args = parser.parse_args()

    qid2query = {}
    sessions = []
    with open('names.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        session_id = 0
        for obj in reader:
            query = obj['query']
            qid = obj[qid]
            qid = int(qid)
            qid2query[qid] = query

    qids = sorted(qid2query.keys())
    for qid in qids:
        args.output_file.write("{0}\t{1}\n".format(qid, qid2query[qid]))
