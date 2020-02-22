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
        self.data = self._prepare_file(self.data)

        self.process_func = getattr(self, self.MODE_BASE)
        print("PRE-PROCESSING:", file, "to", output)

        self.process_include()
        self.process_tokens()

        # remove last \n added while processing
        self.fout.seek(-1, os.SEEK_CUR)
        self.fout.truncate()
        self.fout.close()

    def _prepare_file(self, filedata):
        """Prepare files to process"""

        # clean windows line-breaks
        tmp = re.sub(r'\r\n','\n', filedata)

        return tmp.split('\n')

    def get_mode(self, token):
        """Get section token to active new modes"""

        # we want to ignore any /NUMBER,
        # cause is an enumerator do not start a new section
        if token[0].isdigit():
            return False

        if token in MODES.keys():
            self.process_func = getattr(self, MODES[token])
        else:
            self.process_func = getattr(self, self.MODE_BASE)

        return True

    def pr_default(self, line):
        """Base process, just add current line with \n """

        self.fout.write(line + '\n')

    def pr_ltx(self, line):
        """LTX process, converts \n to #n"""

        if not len(line) or line[-1] == '"' or line[0] == ';':
            self.fout.write(line + '\n')
        else:
            self.fout.write(line + '#n')

    def process_tokens(self):
        """Process tokens for each MODE"""

        for line in self.data:
            # check special case to force just add new line and continue
            if len(line) and line[0] == '/' and self.get_mode(line[1:4]):
                self.pr_default(line)

                continue

            self.process_func(line)

    def process_include(self):
        """Process #include property"""

        newdata = []

        for line in self.data:
            if len(line) and line[0:8] == '#include':
                filepath = line[8:].strip().replace('"', '')
                tmp = codecs.open(filepath, 'r', CHAR_CODE).read()
                tmp = self._prepare_file(tmp)
                newdata += tmp

            else:
                newdata.append(line)

        self.data = newdata
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=f"pre-process dsf files - v{__version__}")
    parser.add_argument('file', type=str, help='original file to preprocess')
    parser.add_argument('-o', '--output-path', required=True, help='destination file-path')
 
    args = parser.parse_args()

    if not os.path.exists(args.file):
        exit("Please specify a valid file using the --file= parameter.")

    if not '.dsf' in args.file.lower():
        exit("file must be an DSF.")

    Preprocessor(args.file, args.output_path)
