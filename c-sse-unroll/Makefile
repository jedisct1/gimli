CC=gcc -O1 -fomit-frame-pointer -march=native -mtune=native

all: test.out speed

test.out: test
	./test > test.out
	cmp test.out test.exp

test: test.c gimli.o
	$(CC) -o test test.c gimli.o

speed: speed.c gimli.o
	$(CC) -o speed speed.c gimli.o

gimli.o: gimli.c
	$(CC) -c gimli.c

clean:
	@echo "cleaning..."
	@rm -r test 2> /dev/null || true
	@rm -r speed 2> /dev/null || true
