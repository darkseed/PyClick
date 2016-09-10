import argparse
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query_file", type=argparse.FileType('r'))
    parser.add_argument("click_model_file")
    parser.add_argument("url_title_segmented_file", type=argparse.FileType('r'))
    parser.add_argument("output_file", type=argparse.FileType('w'))
    args = parser.parse_args()

    # read selected queries
    query2qid = {}
    qid2segmented = {}
    qid = 1
    for line in args.query_file:
        tf, query_segmented = line.strip().split('\t')
        query = ''.join([query_segmented.split(' ')])  # segmented query to original query
        query2qid[query] = qid
        qid2segmented[query] = query_segmented
        qid += 1

    # read click model output first time, gather urls
    url2uid = {}
    uid2title = {}
    uid = 1
    with open(args.click_model_file) as f:
        for line in f:
            query, url, rel_score = line.strip().split(' ')
            if query not in query2qid:
                continue
            url = url.strip()
            if url not in url2uid:
                url2uid[url] = uid
                uid += 1

    # read url title segmented result
    for line in args.url_title_segmented_file:
        url, segmented = line.strip().split('\t')
        if url not in url2uid:
            continue
        uid = url2uid[url]
        uid2title[uid] = segmented

    # read click model output second time, output trec format
    prev_qid = -1
    rank = 1
    with open(args.click_model_file) as f:
        for line in f:
            query, url, rel_score = line.strip().split(' ')
            if query not in query2qid:
                continue
            url = url.strip()
            uid = url2uid[url]
            qid = query2qid[query]
            if qid != prev_qid:
                prev_qid = qid
                rank = 1
            else:
                rank += 1
            score = -rank
            jstr = json.dumps({"query": qid2segmented[qid], "doc": {"title": url + ' ' + uid2title[uid]}})
            args.output_file.write("{0}\tQ0\tsogou-test-{1}\t{2}\t{3} # {4}\n".format(qid, uid, rank, score, jstr))

