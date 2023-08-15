CC = gcc
CFLAGS = -w -D_GNU_SOURCE -g

all: translateAddresses

translateAddresses: memory_address_translation.c
	$(CC) $(CFLAGS) -o translate memory_address_translation.c

clean:
	rm runall translateAddresses