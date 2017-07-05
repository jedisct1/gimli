CC=gcc -O3 -fomit-frame-pointer -march=native -mfpu=neon -marm

all: test.out speed

test.out: test
	./test > test.out
	cmp test.out test.exp

test: test.c gimli.s consts.c
	$(CC) -o test test.c gimli.s consts.c

speed: speed.c gimli.s consts.c cpucycles.c
	$(CC) -o speed speed.c gimli.s consts.c cpucycles.c


%.o: %.s
	$(CC) -c -g -Wall -Wextra $^ -o $@

clean:
	@echo cleaning...
	@rm -r test 2> /dev/null || true
	@rm -r speed 2> /dev/null || true
	@rm -r *.o 2> /dev/null || true

