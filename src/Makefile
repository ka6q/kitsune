#!/bin/sh

all: bench

test: clean-tmp
	: test
	bzcat ../test/silesia/webster.bz2 | ./kitsune ../tmp/sample.kz | wc -c

test-small: clean-tmp
	: test-small
	cat ../test/sample/sample.txt | ./kitsune ../tmp/sample.kz > /dev/null

clean-tmp:
	rm -fr ../tmp/*

clean:
	rm -fr ../tmp/*
	rm -fr __pycache__/

#------------------------------------------------------------------------------
# Benchmarks, Comparisons:
#------------------------------------------------------------------------------

kz: test
	: kz compression ratio
	@( bzcat ../test/silesia/webster.bz2 | wc -c | tr -d '\012' ;\
    echo -n / ;\
    ( gzip < ../tmp/sample.kzd ; cat ../tmp/sample.kz ) | wc -c ;\
  ) | tee /dev/tty | bash -c 'BC_ENV_ARGS=<(echo scale=2) bc'

kz-anisotropic: test
	: kz with 10%..100% redaction, 2..4 number of representations
	 @./redact ../tmp/sample.kzd 

snappy::
	: snappy compression ratio
	@( bzcat ../test/silesia/webster.bz2 | wc -c | tr -d '\012' ;\
     echo -n / ;\
	   bzcat ../test/silesia/webster.bz2 \
     | python -m snappy -c - - | wc -c \
  ) | tee /dev/tty | bash -c 'BC_ENV_ARGS=<(echo scale=2) bc'

gzip1:
	: gzip1 compression ratio
	@( bzcat ../test/silesia/webster.bz2 | wc -c | tr -d '\012' ;\
     echo -n / ;\
	   bzcat ../test/silesia/webster.bz2 | gzip -1 | wc -c \
  ) | tee /dev/tty | bash -c 'BC_ENV_ARGS=<(echo scale=2) bc'

gzip6:
	: gzip6 compression ratio - cf. Parquet default
	@( bzcat ../test/silesia/webster.bz2 | wc -c | tr -d '\012' ;\
     echo -n / ;\
	   bzcat ../test/silesia/webster.bz2 | gzip -6 | wc -c \
  ) | tee /dev/tty | bash -c 'BC_ENV_ARGS=<(echo scale=2) bc'

gzip9:
	: gzip9 compression ratio
	@( bzcat ../test/silesia/webster.bz2 | wc -c | tr -d '\012' ;\
     echo -n / ;\
	   bzcat ../test/silesia/webster.bz2 | gzip -9 | wc -c \
  ) | tee /dev/tty | bash -c 'BC_ENV_ARGS=<(echo scale=2) bc'

bench: kz snappy gzip1 gzip6 gzip9 kz-anisotropic


