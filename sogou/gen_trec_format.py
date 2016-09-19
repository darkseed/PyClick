import argparse
import json
import codecs

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query_file")
    parser.add_argument("click_model_file")
    parser.add_argument("url_title_segmented_file")
    parser.add_argument("output_file", type=argparse.FileType('w'))
    parser.add_argument("output_docid_file", type=argparse.FileType('w'))
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
        print query

    # read click model output first time, gather urls
    url2uid = {}
    uid2title = {}
    uid = 1
    with codecs.open(args.click_model_file, 'r', 'utf-8') as f:
        for line in f:
            line = line.encode("utf-8")
            query, url, rel_score = line.strip().split(' ')
            if query not in query2qid:
                continue
            url = url.strip()
            if url not in url2uid:
                url2uid[url] = uid
                uid += 1
                args.output_docid_file.write("{0}\t{1}\n".format(uid, url))

    # read url title segmented result
    for line in codecs.open(args.url_title_segmented_file, 'r', 'utf-8'):
        line = line.encode("utf-8")
        line = line.strip()
        if not line or '\t' not in line:
            continue 
        url, segmented = line.split('\t')
        if url not in url2uid:
            continue
        uid = url2uid[url]
        uid2title[uid] = segmented

    # read click model output second time, output trec format
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
            if uid not in uid2title or url == "http://weixin.qq.com/":
                continue
            qid = query2qid[query]
            if qid != prev_qid:
                prev_qid = qid
                rank = 1
            else:
                rank += 1
            score = -rank
            obj = {"query": qid2segmented[qid], "doc": {"title": uid2title[uid], "url": url}}
            jstr = json.dumps(obj, ensure_ascii=False)
            args.output_file.write("{0}\tQ0\tsogou-{1}\t{2}\t{3} # {4}\n".format(qid, uid, rank, score, jstr))

