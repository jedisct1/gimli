#include "avr.h"
#include "print.h"

void avr_end()
{
  serial_write(4);
  while(1) {};
}
