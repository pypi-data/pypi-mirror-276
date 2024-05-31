#!/usr/local/bin/python3

from graphe.digraph import digraph
from graphe.digraph import regex
from graphe import draw

import unittest

class TestRegex(unittest.TestCase):

    def test_test(self):
        re = regex.Regex('ABC')

        assert re.match('ABC') == True
        assert re.match('ABD') == False


    def test_dna_motif(self):
        seq = 'ATGTCAGCTAAGCGAATAGTACGT'
        re = regex.Regex('T(A|G)..AT')

        assert re.match(seq) == True


if __name__ == '__main__':
    unittest.main()
