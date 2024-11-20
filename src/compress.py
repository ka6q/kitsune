#!/usr/bin/python

import subprocess
from huffman import HuffmanCoding
import sys
import random

from typing import List

def compress(hfm, gzinta, gzouta, gzdict, parser):
	hist = dict()
	i = 0
	indices = ""
	while True:
		toks = parser(gzinta)
		if toks is None: break
		for f in toks:
			f1 = redact(f)
			if f in hist:
				indices += str(hist[f]) + "\n"
			else:
				hist[f] = i
				#gzdict.write(bytes(str(i)+" ",'utf-8') + f + bytes("\n",'utf-8'))
				gzdict.write(f + bytes("\n",'utf-8'))
				i += 1
				# compute entropy sharing
				if (f1 == f): pass # wip: write (-1) to redacted dict
				else: pass # wip: write redacted literal to redacted dict
	oindices = hfm.compressor(indices)
	gzouta.write(oindices)

def byter(st):
  return bytes(st, 'utf-8')

# simulated parser
def parse_words(gzinta) -> List[str]:
	line = gzinta.readline()
	if not line: return None
	return map(byter, line.split())

# simulated redaction
def redact(word):
	redact_pct = 10
	if (random.random() * 10 < redact_pct):
		return random.random()
	else:
		return word

