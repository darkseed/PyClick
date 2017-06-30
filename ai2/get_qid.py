import argparse
import sys
reload(sys)
sys.setdefaultencoding('UTF8')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("in_query_file", type=argparse.FileType('r'))
    parser.add_argument("start_id", type=int)
    parser.add_argument("output_file", type=argparse.FileType('w'))
    parser.add_argument("--lowercase", "-l", action='store_true')
    args = parser.parse_args()

    qid = args.start_id
    met = set()
    for line in args.in_query_file:
        q = line.strip()
        if args.lowercase:
            q = q.lower()
        if q not in met:
            met.add(q)
            qid += 1
            args.output_file.write('{0}\t{1}\n'.format(qid, q))

