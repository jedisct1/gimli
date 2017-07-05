PREFIX		 ?= arm-none-eabi
CC		  		= $(PREFIX)-gcc
LD		  		= $(PREFIX)-gcc
OBJCOPY			= $(PREFIX)-objcopy
OPENCM3_DIR = ./libopencm3

LDSCRIPT   = ./libopencm3/lib/stm32/l1/stm32l100xc.ld
LIBNAME    = opencm3_stm32l1
ARCH_FLAGS = -mthumb -mcpu=cortex-m3 -msoft-float
DEFINES    = -DSTM32L1
OBJS	   = stm32l1_wrapper.o


CFLAGS	+= -O3 \
		   -Wall -Wextra -Wimplicit-function-declaration \
		   -Wredundant-decls -Wmissing-prototypes -Wstrict-prototypes \
		   -Wundef -Wshadow \
		   -I$(OPENCM3_DIR)/include \
		   -fno-common $(ARCH_FLAGS) -MD $(DEFINES)
LDFLAGS		+= --static -Wl,--start-group -lc -lgcc -lnosys -Wl,--end-group \
		   -T$(LDSCRIPT) -nostartfiles -Wl,--gc-sections \
		   $(ARCH_FLAGS) \
		   -L$(OPENCM3_DIR)/lib

all: lib.installed test/test.bin test/speed.bin

lib.installed:
	touch lib.installed
	git clone https://github.com/libopencm3/libopencm3.git
	@echo make --no-print-directory -C $(OPENCM3_DIR)
	@make --no-print-directory -C $(OPENCM3_DIR) > /dev/null || true

%.bin: %.elf
	@echo OBJCOPY $@
	@$(OBJCOPY) -Obinary $(*).elf $(*).bin

test/test.elf: lib.installed gimli.s test/test.o $(OBJS) $(LDSCRIPT)
	@echo LD $@
	@$(LD) -o test/test.elf gimli.s test/test.o $(OBJS) $(LDFLAGS) -l$(LIBNAME)

test/speed.elf: lib.installed gimli.s test/speed.o $(OBJS) $(LDSCRIPT)
	@echo LD $@
	@$(LD) -o test/speed.elf gimli.s test/speed.o $(OBJS) $(LDFLAGS) -l$(LIBNAME)

.PHONY: gimli.s

gimli.s: gen_gimli.py
	@echo GEN $@
	@./gen_gimli.py > $@

clean:
	@echo "rm *.o *.bin *.elf *.d"
	@rm -f test/*.bin 2> /dev/null || true
	@rm -f test/*.elf 2> /dev/null || true
	@rm -f test/*.d 2> /dev/null || true
	@rm -f test/*.o 2> /dev/null || true
	@rm -f *.bin 2> /dev/null || true
	@rm -f *.elf 2> /dev/null || true
	@rm -f *.d 2> /dev/null || true
	@rm -f *.o 2> /dev/null || true

distclean: clean
	@echo "rm -fr libopencm3"
	@rm lib.installed 2> /dev/null || true
	@rm -fr libopencm3 2> /dev/null || true

archclean: distclean
	@echo "rm gimli.s"
	@rm gimli.s  2> /dev/null || true