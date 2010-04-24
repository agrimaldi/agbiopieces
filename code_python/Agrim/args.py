#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import optparse
import copy
sys.path.append(os.path.join(os.environ['BP_DIR'], 'code_python'))

bp_dir = os.environ['BP_DIR']


class BioPiece_OptionParser(optparse.OptionParser):
    def __init__(self):
        optparse.OptionParser.__init__(self)
        self.bp_name = self.get_prog_name()
        self.usage_path = os.path.join(bp_dir, 'bp_usage', self.bp_name+'.wiki')

    def print_usage(self, file=sys.stderr):
        os.system('print_wiki -i %s' % (self.usage_path))

    def print_help(self, file=sys.stderr):
        os.system('print_wiki -i %s %s' % (self.usage_path, '--help'))

    def error(self, msg):
        self.print_usage()
        raise Exception, "%s: error: %s\n" % (self.get_prog_name(), msg)


class Reader_OptionParser(BioPiece_OptionParser):
    def __init__(self):
        BioPiece_OptionParser.__init__(self)
        self.add_option('-i', '--data_in', dest='data_in',
                        help='Comma separated list of files or glob' \
                        'expression to read.')
        self.add_option('-I', '--stream_in', dest='stream_in',
                        action='store_true', default=False,
                        help='Read input from stream file  - Default=STDIN')
        self.add_option('-n', '--num', dest='num', type='int',
                        help='Limit number of records to read.')
        self.add_option('-?', default=False, dest='usage', action='store_true',
                        help='Print full usage description.')
        self.set_defaults(num = None)
            
        
def is_glob(sstr):
    glob_symbols = set(['[', ']', '!', '?', '*'])
    for c in sstr:
        if c in glob_symbols:
            return True
    return False
