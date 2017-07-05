1# fast implementation of gimli

### Size:

    avr-size obj/gimli.o
    text    data     bss     dec     hex filename
    20938       0       0   20938    51ca obj/gimli.o

### Speed:

    test/speed_atmega2560.sh
    array initialized !
    gimli: 11322 11322 11322 11322 11322 11322 11322 11322 11322

### Stack:

    test/stack_atmega2560.sh
    gimli : 45 stack bytes
