#include "../stm32wrapper.h"
#include <stdio.h>
#include <stdint.h>
#include "../gimli.h"

int main(void)
{
    clock_setup();
    gpio_setup();
    usart_setup(115200);

    char str[100];
    uint32_t x[12];
    int i;
    const unsigned char term=4;

    for (i = 0;i < 12;++i) x[i] = i * i * i + i * 0x9e3779b9;

    fflush(stdout);
    for (i = 0; i < 100000; i++)
      __asm__("NOP");


    for (i = 0;i < 12;i+=4) {
        sprintf(str, "%08lx %08lx %08lx %08lx\n", x[i], x[i+1], x[i+2], x[i+3]);
        send_USART_str(str);
    }

    send_USART_str("----------------------\n");

    gimli(x);

    for (i = 0;i < 12;i+=4) {
        sprintf(str, "%08lx %08lx %08lx %08lx\n", x[i], x[i+1], x[i+2], x[i+3]);
        send_USART_str(str);
    }
    send_USART_str("----------------------\n");
    send_USART_str("Done!\n");

    send_USART_bytes(&term,1);

    while(1);
    return 0;
}
