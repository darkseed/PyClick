import argparse
import random
import numpy as np
import sys
import os
reload(sys)
sys.setdefaultencoding('UTF8')
import re


def gen_old2new(docid2url_file_path):
    np.random.seed(0)
    docids = []
    with open(docid2url_file_path) as f:
        for line in f:
            docid, url = line.split('\t')
            docids.append(docid)
    new_docids = np.random.choice(docids, len(docids), replace=False)
    return dict(zip(docids, new_docids))


def change_old(file_path, output_file_path, old2new):
    def docidreplace(matchobj):
        return old2new[matchobj.group(0)]
    with open(file_path) as f, open(output_file_path, 'w') as fout:
        for line in f:
            re.sub(r'sogou-[0-9]+', docidreplace, line)
            fout.write(line)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("old_dir")
    parser.add_argument("new_dir")
    args = parser.parse_args()

    docid2url_file_path = os.path.join(args.old_dir, "docid2url")
    old2new = gen_old2new(docid2url_file_path)
    for fname in ["docid2url", "sample1k.SDBN.qrels", "sample1k.trec",  "sdbn.qrels"]:
        p = os.path.join(args.old_dir, fname)
        op = os.path.join(args.new_dir, fname)
        change_old(p, op, old2new)




