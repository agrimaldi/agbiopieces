#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.environ['BP_DIR'], 'code_python'))
from xml.etree.cElementTree import iterparse
from Agrim.base_bp import *


class BlastXMLParser:
    '''A parser for XML formatted blast outputs.
    
    @keyparam `infile`: Path to the file.
    @keyparam `num`: Maximum number of records to output.
    '''
    def __init__(self, infile=None, num=None):
        '''Constructor.
        '''
        self._infile = infile
        self._keys = set(('Iteration_query-def', 'Hit_id', 'Hsp_identity',
                          'Hsp_align-len', 'Hsp_gaps', 'Hsp_query-from',
                          'Hsp_query-to', 'Hsp_hit-from', 'Hsp_hit-to',
                          'Hsp_evalue','Hsp_bit-score', 'Hsp_positive',
                          'Hsp_qseq', 'Hsp_hseq', 'Hsp_midline'))
        self._num = num
        self._cnum = 0

    def _attr_from_tag(self, key):
        '''Get the name of the attribute from the corresponding XML tag.
        '''
        output = key.replace('-', '_')
        return '_' + output.lower()

    def parse(self):
        '''Main parsing method.

        A record is output at each time a closing `Hsp` tag is read.
        '''
        for event, node in iterparse(self._infile):
            if node.tag in self._keys:
                setattr(self, self._attr_from_tag(node.tag), node.text)
            if node.tag == 'Hsp':
                yield BlastHitRecord(q_id=self._iteration_query_def,
                                     s_id=self._hit_id, n_ident=self._hsp_identity,
                                     align_len=self._hsp_align_len,
                                     gaps=self._hsp_gaps, s_beg=self._hsp_hit_from,
                                     q_beg=self._hsp_query_from,
                                     q_end=self._hsp_query_to,
                                     s_end=self._hsp_hit_to, e_val=self._hsp_evalue,
                                     bit_score=self._hsp_bit_score,
                                     positive=self._hsp_positive,
                                     q_seq=self._hsp_qseq, s_seq=self._hsp_hseq,
                                     m_seq=self._hsp_midline)
                self._cnum += 1
                if self._cnum == self._num:
                    return
            node.clear()


class BlastHitRecord(BioPiecesRecord):
    '''Class representing a record of a blast hit.
    '''
    def __init__(self, q_id=None, s_id=None, n_ident=None, align_len=None,
                 gaps=None, q_beg=None, q_end=None, s_beg=None, s_end=None,
                 e_val=None, bit_score=None, positive=None, q_seq=None,s_seq=None,
                 m_seq=None):
        kwargs = locals()
        del kwargs['self']
        BioPiecesRecord.__init__(self, **kwargs)
        self.REC_TYPE = 'BLAST'
        if int(self.S_BEG) > int(self.S_END):
            self.STRAND = '-'
            tmp = self.S_BEG
            self.S_BEG = self.S_END
            self.S_END = tmp
        else:
            self.STRAND = '+'
        self.MISMATCHES = str(count_chars(self.M_SEQ, ' +'))
        self.IDENT = str(float(self.N_IDENT)/float(self.ALIGN_LEN) * 100)
        self.Q_BEG = str(int(self.Q_BEG)-1)
        self.Q_END = str(int(self.Q_END)-1)
        self.S_BEG = str(int(self.S_BEG)-1)
        self.S_END = str(int(self.S_END)-1)


def main():

    h = BlastXMLParser('/Users/sopo/Desktop/xmlbiopieces/blastout.xml')
    h.parse()

if __name__ == '__main__':
    main()
