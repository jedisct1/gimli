#include "../stm32wrapper.h"
#include "../gimli.h"
#include <stdint.h>
#include <stdio.h>

#define NRUNS 20

int main(void)
{
  clock_setup();
  gpio_setup();
  usart_setup(115200);
  unsigned long long t[NRUNS];
  char output[32];
  int i;
  const unsigned char term=4;
  uint32_t state[12];


  // plainly reading from CYCCNT is more efficient than using the
  // dwt_read_cycle_counter() interface offered by libopencm3,
  // as this adds extra overhead because of the function call

  SCS_DEMCR |= SCS_DEMCR_TRCENA;
  DWT_CYCCNT = 0;
  DWT_CTRL |= DWT_CTRL_CYCCNTENA;

  fflush(stdout);
  for (i = 0; i < 100000; i++)
    __asm__("NOP");

  // Report cycle counts for no function
  for(i=0;i<NRUNS;i++)
  {
    t[i] =  DWT_CYCCNT;
  }

  for(i=0;i<NRUNS-i;i++)
  {
    sprintf(output, "%llu ", t[i+1]-t[i]);
    send_USART_str(output);
  }

  send_USART_str("\n");


  // Report cycle counts for gimli
  for(i=0;i<NRUNS;i++)
  {
    t[i] =  DWT_CYCCNT;
    gimli(state);
  }

  for(i=0;i<NRUNS-i;i++)
  {
    sprintf(output, "%llu ", t[i+1]-t[i]);
    send_USART_str(output);
  }

  send_USART_str("\n");

  // Hang up terminal
  send_USART_bytes(&term,1);

  while (1);

  return 0;
}
