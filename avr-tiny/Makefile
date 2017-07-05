TARGET_DEVICE=atmega2560
CPUFREQ=16000000
CC=/usr/bin/avr-gcc
OBJCOPY=/usr/bin/avr-objcopy
AR=/usr/bin/avr-ar
STRIP=/usr/bin/avr-strip

CFLAGS  = -g -Wall -Wextra -Werror -mmcu=$(TARGET_DEVICE) -O3 -I../randombytes/ -I.. -I./include/ -DF_CPU=$(CPUFREQ) -mcall-prologues

all: test/test.hex test/speed.hex test/speed_hash.hex test/stack.hex

GIMLI = obj/gimli.o

TEST = 	test/print.c \
		test/avr.c \
		test/fail.c

SPEED = test/print.c \
		test/avr.c \
		test/fail.c \
		test/cpucycles.c

STACK = test/print.c \
		test/avr.c \
		test/fail.c

.PHONY: gimli.s test/test.c test/speed.c test/stack.c clean

gimli.s:
	@echo GEN $@
	@./gen_gimli.py > $@

test/test.c:
	@echo GEN $@
	@./test/gen_test.py > $@

test/speed.c:
	@echo GEN $@
	@./test/gen_speed.py > $@

test/stack.c:
	@echo GEN $@
	@./test/gen_stack.py > $@

test/test: test/test.c obj/gimli.a $(TEST)
	@echo CC $@
	@$(CC) $(CFLAGS) $^ -o $@

test/speed: test/speed.c obj/gimli.a $(SPEED)
	@echo CC $@
	@$(CC) $(CFLAGS) $^ -o $@

test/stack: test/stack.c obj/gimli.a $(TEST)
	@echo CC $@
	@$(CC) $(CFLAGS) $^ -o $@

test/speed_hash: test/speed_hash.c gimli.s gimli_hash.c $(SPEED)
	@echo CC $@
	@$(CC) $(CFLAGS) $^ -o $@

test/%.hex: test/%
	@echo OBJCOPY $@
	@$(OBJCOPY) -O ihex -R .eeprom $^ $@

obj/gimli.a: $(GIMLI)
	@echo AR $@
	@$(AR) -ar cr $@ $^

obj/gimli.o: gimli.s
	@echo CC $@
	@mkdir -p obj/
	@$(CC) $(CFLAGS) -c $^ -o $@

clean:
	@echo "cleaning..."
	@rm -r obj/* 2> /dev/null || true
	@rm -r test/test 2> /dev/null || true
	@rm -r test/speed 2> /dev/null || true
	@rm -r test/speed_hash 2> /dev/null || true
	@rm -r test/stack 2> /dev/null || true
	@rm -r test/test.c 2> /dev/null || true
	@rm -r test/speed.c 2> /dev/null || true
	@rm -r test/stack.c 2> /dev/null || true
	@rm -r gimli.s 2> /dev/null || true
