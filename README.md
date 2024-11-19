# Anisotropic Compression

While there is not a manadatory requiremeent that the parallel streams be in
lock step for correctness in our algorithm, typical analytic data-warehouse
data does invariable have multiple such streams, each one is derived from
the a parent stream after some encrichment, redaction, tokenization or other
data prep. Such streams tend to have entropy which stays largely in sync;
and this is the extra boost which we exploit to obtain higher compression
ratios in anisotropic compression.

Notes: Unlike traditional compression/decompession algorithms which
operate on a simple stream of bytes as input, anisotropic compression is
delayered with the parser. Therefore it operates on a stream of parse
tokens. Consequently, the decompression is a series of tokens. The ETL
parser and columnar file format. eg.  Paraquet, will control the nature
of this tokenization

# Benchmarks:

Compression ratio benchmarks compare well with currently common compression
algorithms. `kz` is Kitsune anisotropic compression. `snappy` and `gzip-6`
are commonly used in the industry in `Parquet` files.

Conventional compression algorithms only compress one stream at a
time. Anisotropic compression compresses multiple synchronous representations
together, benefiting from the implicit sharing of entropy between the
parallel streams.

First, in order to obtain a simple apples to apples comparison, we compare
a baseline against conventional compression algorithms, we compare the
performance of anistropic compression for a single representation of data.

## Single representation:

Selected files from the Silesia compression corpus were tested.
[https://sun.aei.polsl.pl/~sdeor/index.php?page=silesia]. The file 
`webster.bz2`, 41 MB in size (roughly comparable to one Parquet block at the 
smallest choice of 64MB) is chosen for the following tests.

```
Ratio: 3.28x, Compressed size: 12631274, : kz
Ratio: 2.05x, Compressed size: 20218182, : snappy
Ratio: 2.76x, Compressed size: 14977096, : gzip1
Ratio: 3.39x, Compressed size: 12201972, : gzip6 - cf. Parquet default
Ratio: 3.43x, Compressed size: 12061616, : gzip9
```

As can be seen above, the compression ratios (3.28x againt 3.39x) are
very competitive  with gzip level 6 (the default compression in Parquet).
Yet the compression and decompression speed is expected to be closer to
Snappy than to gzip due to the delayered hashing of token based history
buffer. (For CPU performance optimized code, please contact the author).

For reference, typically expected compression ratios from benchmarks of
various compression algoriths are as follows:

```
[https://github.com/valamidev/nodejs-js-compress-benchmark]
Original length(buffer): 565447, Original length(text):558152
Node-snappy/SnappyJS - Ratio: 0.599 (1.67x) Compressed size: 338492
Lz4 -                  Ratio: 0.705 (1.42x) Compressed size: 398611
Gzip-default -         Ratio: 0.366 (2.73x) Compressed size: 206705
Gzip-Level=1 -         Ratio: 0.415 (2.41x) Compressed size: 234501
Brotli-default -       Ratio: 0.29  (3.44x) Compressed size: 164113
Brotli-Quality=0 -     Ratio: 0.439 (2.28x) Compressed size: 248108
```

## Multiple representations:

Benchmarks for multiple representation depend on a number of different
factors: What the secondary representations are, for eg, how redaction
or enrichment is done. And how many representations there are. And if
the differen representations are under different encryption keys (for
access-control reasons).

This is very data and application dependent.  However, here are few sample
benchmarks. The following use-cases are simulated:

```
Representation 1: original data
Representation 2: tokenized data (data replaced by a random number)
Representation 3: above tokenized data enriched, simulated by rounding/1000.
Representation 4: original text data with some textual enrichments
```

For the purposes of this demo, Representation 1 is assumed privileged
and compressed and encrypted separately. Representations 2 through 4 are
assumed in the same lower privilege of access, and are compressed together.

The ratio of data which is redaction are tested between 5% to 80%.  100%
redaction  is essentially the same as tokenization (commonly used for PII
masking in analytic workloads).

```
reps=2 redact=5% 3.53x
reps=3 redact=5% 5.27x
reps=4 redact=5% 6.98x

reps=2 redact=10% 3.50x
reps=3 redact=10% 5.20x
reps=4 redact=10% 6.85x

reps=2 redact=20% 3.46x
reps=3 redact=20% 5.09x
reps=4 redact=20% 6.62x

reps=2 redact=40% 3.40x
reps=3 redact=40% 4.91x
reps=4 redact=40% 6.25x

reps=2 redact=80% 3.33x
reps=3 redact=80% 4.64x
reps=4 redact=80% 5.70x

reps=2 redact=100% 3.36x
reps=3 redact=100% 4.59x
reps=4 redact=100% 5.51x

```

As can be seem above, as the number of representations increases, one can
expect the compression ratio benefits to increase as well. This is the main
idea behind anisotropic compression. Each new representation only occupies
an incremental amount of space on disk, even though when you decompress,
you obtain a different column of values for each representation.

# Publications and Disclosures:

The following publications are disclosed.

### Entropy Sharing Across Multiple Compression Streams

Abstract: According to one or more embodiments, multiple related data
streams are compressed jointly, such that substantive similarities between
the multiple related streams are leveraged to reduce the overall size of
the resulting compressed data. Specifically, given the compressed version
of a primary data stream, a secondary data stream may be highly compressed
by utilizing portions of the compressed version of the primary data stream
to represent similar portions of the secondary data stream. A compression
application is configured to receive (either concurrently or separately)
information identifying multiple related input streams. For each input stream
provided to the compression application, the application outputs one output
stream. The computing system writes the output streams of the compression
application to storage. Embodiments allow the size of the compressed
version of a secondary data stream to be greatly reduced compared to the
size of the stream compressed without reference to a primary data stream.

```
Patent number: 10681106
Filed: February 28, 2018. Granted: June 9, 2020.
Inventors: Shrikumar Hariharasubrahmanian, Michael Delorimier
```

### Anisotropic Compression As applied to Columnar Storage Formats

Abstract: Herein are spatially scalable techniques for anisotropic
compression of shared entropy between alternate representations of same
data.  In an embodiment, a computer compresses an uncompressed independent
column into a compressed independent column. Based on the compressed
independent column, an uncompressed dependent column is compressed into
a compressed dependent column.  The compressed independent column and the
compressed dependent column are stored in a same file. In an embodiment,
a computer stores, in metadata, an encrypted private key for decrypting
an encrypted column. The encrypted column and the metadata are stored in
a file. A request to read the encrypted column is received. Based on a
public key and the file, the encrypted private key is decrypted into a
decrypted private key. The public key is contained in the request and/or
the file. The request is executed by decrypting, based on the decrypted
private key and the file, the encrypted column.

```
Patent number: 11562085
Filed: October 17, 2019. Granted: January 24, 2023.
Inventors: Shrikumar Hariharasubrahmanian, Jean-Pierre Dijcks, Jacco Draaijer
```


