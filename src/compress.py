#!/usr/bin/python

import subprocess
from huffman import HuffmanCoding
import sys

from typing import List

def compress(hfm, gzinta, gzouta, gzdict, parser):
	hist = dict()
	i = 0
	indices = ""
	while True:
		toks = parser(gzinta)
		if toks is None: break
		for f in toks:
			if f in hist:
				indices += str(hist[f]) + "\n"
			else:
				hist[f] = i
				#gzdict.write(bytes(str(i)+" ",'utf-8') + f + bytes("\n",'utf-8'))
				gzdict.write(f + bytes("\n",'utf-8'))
				i += 1
	oindices = hfm.compressor(indices)
	gzouta.write(oindices)

def byter(st):
  return bytes(st, 'utf-8')

def parse_words(gzinta) -> List[str]:
	line = gzinta.readline()
	if not line: return None
	return map(byter, line.split())

#decom_path = h.decompress(output_path)

