import codecs
import argparse

__author__ = 'Zhuyun Dai'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename")
    parser.add_argument("output_filename")
    args = parser.parse_args()

    with codecs.open(args.input_filename, 'r', 'euc-cn', errors='replace') as input_file, open(args.output_filename, 'w') \
            as output_file:
        for line in input_file:
            line = line.encode('utf-8')
            output_file.write(line)
