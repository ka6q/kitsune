#!/usr/bin/python

import subprocess
from huffman import HuffmanCoding
import sys

from typing import List

def decompress(hfm, gzinta, gzouta):
	indices = hfm.decompressor(gzinta)

	hist = dict()
	num = 0
	with open(gzinta + "d", "rb") as gzdict:
		for line in gzdict:
			hist[num] = line
			num += 1
	for f in indices.split():
		gzouta.write(unbyter(hist[int(f)]))

def unbyter(st):
	return (st.decode('utf-8'))


