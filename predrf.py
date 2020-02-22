#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re
import argparse
import codecs

__author__ = 'David Colmenero (D_Skywalk) @ http://david.dantoine.org'
__version__ = '0.1.0'

CHAR_CODE = 'iso-8859-1'
MODES = {
    'LTX': 'pr_ltx',
}

class Preprocessor(object):

    MODE_BASE = "pr_default"
    process_func = None

    def __init__(self, file, output):
        self.fout = codecs.open(output, 'w', CHAR_CODE)
        self.data = codecs.open(file, 'r', CHAR_CODE).read()
        self.data = self._clean_file(self.data)
        
        self.process_func = getattr(self, self.MODE_BASE)
        print("PRE-PROCESSING:", file, "to", output)

        self.process_include()
        self.process_tokens()

        #remove last \n
        self.fout.seek(-1, os.SEEK_CUR)
        self.fout.truncate()
        self.fout.close()
        
    def _clean_file(self, filedata):
        # clean windows line-breaks
        tmp = re.sub(r'\r\n','\n', filedata)
        
        return tmp.split('\n')

    def get_mode(self, token):
        if token[0].isdigit():
            return False

        if token in MODES.keys():
            self.process_func = getattr(self, MODES[token])
        else:
            self.process_func = getattr(self, self.MODE_BASE)

        return True

    def pr_ltx(self, line):
        if not len(line) or line[-1] == '"' or line[0] == ';':
            self.fout.write(line + '\n')
        else:
            self.fout.write(line + '#n')

    def pr_default(self, line):
        self.fout.write(line + '\n')

    def process_tokens(self):
        for line in self.data:
            if len(line) and line[0] == '/' and self.get_mode(line[1:4]):
                self.pr_default(line)
                continue
            
            self.process_func(line)

    def process_include(self):
        newdata = []
        for line in self.data:
            if len(line) and line[0:8] == '#include':
                filepath = line[8:].strip().replace('"', '')
                tmp = codecs.open(filepath, 'r', CHAR_CODE).read()
                tmp = self._clean_file(tmp)
                newdata += tmp
            else:
                newdata.append(line)
        self.data = newdata
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='original file to preprocess')
    parser.add_argument('-o', '--output-path', required=True, help='destination file-path')
 
    args = parser.parse_args()
    if not os.path.exists(args.file):
        exit("Please specify a valid file using the --file= parameter.")

    if not '.dsf' in args.file.lower():
        exit("file must be an DSF.")

    Preprocessor(args.file, args.output_path)
