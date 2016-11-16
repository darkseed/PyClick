import argparse
import random
import sys
import os
import re

reload(sys)
sys.setdefaultencoding('UTF8')

def read_old2new(old2new_file_path):
    old2new = {}
    with open(old2new_file_path) as f:
        for line in f:
            old, new = line.strip().split('\t')
            old2new[old] = new
    return  old2new

def gen_old2new(docid2url_file_path):
    random.seed(0)
    docids = []
    with open(docid2url_file_path) as f:
        for line in f:
            docid, url = line.split('\t')
            docids.append(docid)
    new_docids = list(docids)
    random.shuffle(new_docids)
    return dict(zip(docids, new_docids))


def change_old(file_path, output_file_path, old2new):
    def docidreplace(matchobj):
        return old2new[matchobj.group(0)]
    with open(file_path) as f, open(output_file_path, 'w') as fout:
        for line in f:
            res = re.sub(r'sogou-[0-9]+', docidreplace, line)
            fout.write(res)
    return

def rerank_old(file_path, output_file_path, old2new):
    data = []
    with open(file_path) as f:
        for line in f:
            info, comment = line.strip().split('#')
            qid, tmp, oldid, tmp2, score = info.split('\t')
            score = float(score)
            qid = int(qid)
            data.append((qid, old2new[oldid.strip()], score))
    data.sort(key=lambda item: (int(item[0]), -item[2]))

    with open(output_file_path) as fout:
        prev_qid = -1
        r = 0
        for qid, docno, score in data:
            if qid != prev_qid:
                r = 0
            r += 1
            fout.write("{0}\tQ0\t{1}\t{3} # {4}\n".format(qid, docno, r, score, comment))
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("old_dir")
    parser.add_argument("new_dir")
    parser.add_argument("--old2new_file_path", "-o", type=str, default=None)
    parser.add_argument("--rerank", "-r", action="store_true")
    args = parser.parse_args()

    if args.old2new_file_path:
        docid2url_file_path = os.path.join(args.old_dir, "docid2url")
        old2new = gen_old2new(docid2url_file_path)
        with open(os.path.join(args.new_dir, "oldid2newid"), 'w') as fout:
            for old, new in old2new.items():
                fout.write("{0}\t{1}\n".format(old, new))
    else:
        old2new = read_old2new(args.old2new_file_path)

    if not args.rerank:
        for fname in ["docid2url", "sample1k.SDBN.qrels", "sample1k.trec",  "sdbn.qrels"]:
            p = os.path.join(args.old_dir, fname)
            op = os.path.join(args.new_dir, fname)
            change_old(p, op, old2new)
    else:
        for fname in ["bm25.trec", "click_emb_avg.trec",  "emb_avg.trec",  "lm_jm.trec",  "random.trec", "bool_and.trec",
                      "coordinate.trec",    "lm_dir.trec",   "lm.trec",   "tf_idf.trec"]:
            p = os.path.join(args.old_dir, fname)
            op = os.path.join(args.new_dir, fname)
            rerank_old(p, op, old2new)







