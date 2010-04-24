#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.environ['BP_DIR'], 'code_python'))
import re
from datetime import datetime
import time
import cStringIO
import logging

bp_log = os.path.join(os.environ['BP_LOG'], 'biopieces.log')
RECORD_SEPARATOR = '\n---'

class BioPiecesRecordList(list):
    def __init__(self):
        pass

    def display(self):
        for rec in self:
            sys.stdout.write(str(rec))


class BioPiecesRecord:
    def __init__(self, **kwargs):
        for param, val in kwargs.items():
            setattr(self, param.upper(), val)

    def __str__(self):
        return '\n'.join([key + ': ' + self.__dict__[key] \
                          for key in self.__dict__]) + RECORD_SEPARATOR


class BioPieceLogger:
    '''Class to handle logging of biopieces runs.

    Usage:
        logger = BioPieceLogger()
        logger.start()
        ...
        logger.end(0)
    '''
    def __init__(self):
        self._cline = os.path.basename(sys.argv[0]) + ' ' + ' '.join(sys.argv[1:])
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.INFO)
        self._filehandler = logging.FileHandler(bp_log, mode='a')
        self._filehandler.setFormatter(logging.Formatter('%(message)s'))
        self._logger.addHandler(self._filehandler)
        self._start_time = ''
        self._datefmt = '%Y-%m-%d %H:%M:%S'
        
    def start(self):
        '''Start monitoring.
        '''
        self._start_time = datetime.now()

    def end(self, status):
        '''Stop monitoring. Generate the log and write it.
        '''
        if not status:
            status = 'OK'
        else:
            status = 'ERROR'
        end_time = datetime.now()
        elapsed = str(end_time - self._start_time).split('.')[0]
        if elapsed.startswith('0'):
            elapsed = '0' + elapsed
        msg = '\t'.join([self._start_time.strftime(self._datefmt),
                         end_time.strftime(self._datefmt), elapsed,
                         os.environ['LOGNAME'], status, self._cline])
        self._logger.info(msg)


def count_chars(sstr, chars):
    return len([c for c in sstr if c in chars])

def removelines(infile, pattern):
    regex = re.compile(pattern)
    output = cStringIO.StringIO()
    with open(infile) as iff:
        for line in iff:
            if not regex.search(line):
                    output.write(line)
    output.seek(0)
    return output

