import argparse
import json
import codecs

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query_file")
    parser.add_argument("click_model_file")
    parser.add_argument("url_title_segmented_file")
    parser.add_argument("docid_file")
    parser.add_argument("model")
    parser.add_argument("output_file", type=argparse.FileType('w'))
    args = parser.parse_args()

    # read selected queries
    query2qid = {}
    qid2segmented = {}
    qid = 1
    for line in codecs.open(args.query_file, 'r', 'utf-8'):
        line = line.encode("utf-8")
        tf, query_segmented = line.strip().split('\t')
        query = ''.join(query_segmented.split(' '))  # segmented query to original query
        query2qid[query] = qid
        qid2segmented[qid] = query_segmented
        qid += 1

    # read uid <=> url
    url2uid = {}
    uid2title = {}
    uid = 1
    with codecs.open(args.docid_file, 'r', 'utf-8') as f:
        for line in f:
            line = line.encode("utf-8")
            uid, url = line.strip().split('\t')
            url2uid[url] = uid

    # get score distributions 
    scores = []
    with codecs.open(args.click_model_file, 'r', 'utf-8', errors="replace") as f:
        for line in f:
            line = line.encode("utf-8")
            query, url, rel_score = line.strip().split(' ')
            if query not in query2qid:
                continue
            url = url.strip()
            uid = url2uid[url]
            #if uid not in uid2title:
            #    print uid, url
            if url == "http://weixin.qq.com/":
                continue
            rel_score = float(rel_score)
            scores.append(rel_score)
    scores = sorted(scores)
    n = float(len(scores))
    a1 = scores[int(n * 0.77)]
    a2 = scores[int(n * 0.93)]
    a3 = scores[int(n * 0.98)]
    a4 = scores[int(n * 0.99)]
    print a1, a2, a3, a4
        

    # read click model output , output trec qrels
    prev_qid = -1
    rank = 1
    with codecs.open(args.click_model_file, 'r', 'utf-8', errors="replace") as f:
        for line in f:
            line = line.encode("utf-8")
            query, url, rel_score = line.strip().split(' ')
            if query not in query2qid:
                continue
            url = url.strip()
            uid = url2uid[url]
            #if uid not in uid2title:
            #    print uid, url
            if url == "http://weixin.qq.com/":
                continue
            qid = query2qid[query]
            if qid != prev_qid:
                prev_qid = qid
            rel_score = float(rel_score)
            rel = 0
            if args.model == "SDBN":
                # old: 0 0.25 0.5 1
                if rel_score <= 0.17:
                    continue
                elif 0.17 < rel_score <= 0.25:
                    rel = 1
                elif 0.25 < rel_score <= 0.37:
                    rel = 2
                elif 0.37 < rel_score <= 0.50:
                    rel = 3
                elif 0.50 < rel_score:
                    rel = 4

            if args.model == "PBM":
                if rel_score <= 0.1978:
                    continue
                elif 0.1978 < rel_score <= 0.4652:
                    rel = 1
                elif 0.4653 < rel_score <= 0.7326:
                    rel = 2
                elif 0.7326 < rel_score:
                    rel = 3

            if args.model == "DCTR":
                if rel_score < a1:
                    continue
                elif rel_score < a2:
                    rel = 1
                elif rel_score < a3:
                    rel = 2
                elif rel_score <= a4:
                    rel = 3
                elif a4 < rel_score:
                    rel = 4

            args.output_file.write("{0}\tQ0\tsogou-{1}\t{2} \n".format(qid, uid, rel))

