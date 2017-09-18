import argparse
import json
import codecs
import csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("log_file")
    parser.add_argument("click_model_file")
    parser.add_argument("output_file", type=argparse.FileType('w'))
    args = parser.parse_args()

    qid2queries = {}
    docid2info = {}
    with open(args.log_file) as f:
        reader = csv.DictReader(f)
        for obj in reader:
            qid = int(obj['qid'])
            query = obj['query']
            qid2queries[qid] = query
            for rank in range(1, 21):
                docid = obj['docno_{0}'.format(rank)]
                title = obj['title_{0}'.format(rank)]
                snippet = obj['snippet_{0}'.format(rank)]
                url = obj['url_{0}'.format(rank)]
                tmp = {"title": title, "url": url, "docid": docid, "snippet": snippet}
                docid2info[docid] = tmp


    # read click model output, output trec format
    prev_qid = -1
    rank = 1
    with codecs.open(args.click_model_file, 'r', 'utf-8', errors="replace") as f:
        for line in f:
            line = line.encode("utf-8")
            items = line.strip().split(' ')
            docid, rel_score = items[-2], items[-1]
            qid = int(items[0])
            query = qid2queries[qid]
            if qid != prev_qid:
                prev_qid = qid
                rank = 1
            else:
                rank += 1
            score = rel_score
            obj = {"query": query, "doc": docid2info[docid]}
            jstr = json.dumps(obj)
            args.output_file.write("{0}\tQ0\t{1}\t{2}\t{3} # {4}\n".format(qid, docid, rank, score, jstr))

