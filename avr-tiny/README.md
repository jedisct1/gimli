# tiny implementation of gimli

### Size:

    avr-size obj/gimli.o
    text    data     bss     dec     hex filename
    1098         0       0    1098     44a obj/gimli.o

### Speed:

    test/speed_atmega2560.sh
    array initialized !
    gimli: 20445 20445 20445 20445 20445 20445 20445 20445 20445

### Stack:

    test/stack_atmega2560.sh
    gimli : 239 stack bytes
