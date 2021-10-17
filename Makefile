CC = clang
CFLAGS = -Wall -Werror -Wextra -pedantic

OPENSSL_BASE = /Users/guptashark/Documents/progs/openssl

INCLUDE = $(OPENSSL_BASE)/include
LIB_PATH = $(OPENSSL_BASE)/lib

all: client.o
	$(CC) -L $(LIB_PATH) -lcrypto -lssl client.o

client.o: client.c
	$(CC) $(CFLAGS) -I $(INCLUDE) -c client.c -o client.o
