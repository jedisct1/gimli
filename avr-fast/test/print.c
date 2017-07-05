#include "print.h"
#include <stdio.h>
#include <avr/io.h>

#ifndef F_CPU
#warning "F_CPU is not defined, set to 16MHz per default."
#define F_CPU 16000000
#endif

//#define BAUD 57600
#define BAUD 38400
#include <util/setbaud.h>

#ifndef UCSRB
# ifndef UDRE
# define UDRE UDRE0
# define RXEN RXEN0
# define TXEN TXEN0
# endif
# ifdef UCSR0A /* ATmega128 */
# define UCSRA UCSR0A
# define UCSRB UCSR0B
# define UBRRL UBRR0L
# define UBRRH UBRR0H
# define UDR UDR0
# else /* ATmega8 */
# define UCSRA USR
# define UCSRB UCR
# endif
#endif


#ifndef UBRR
# define UBRR UBRRL
#endif

static char serial_initialized = 0;

void serial_init(void)
{
  UBRRH = UBRRH_VALUE;
  UBRRL = UBRRL_VALUE;
  /* Enable */
  UCSRB = (1 << RXEN) | (1 << TXEN);
}

void serial_write(unsigned char c)
{
  if(!serial_initialized)
  {
    serial_init();
    serial_initialized = 1;
  }
  while (!(UCSRA & (1 << UDRE))){};
  UDR = c;
}

void print(const char *s)
{
  while(*s != 0)
  {
    serial_write(*s);
    s++;
  }
}

void print_bytes(const unsigned char *x, unsigned int xlen)
{
  unsigned int i;
  char ts[4];
  for (i=0; i<xlen; i++)
  {
    sprintf(ts, "%02x ",x[i]);
    print(ts);
  }
}

void printllu(unsigned long long x)
{
  char str[24];
  int i = 22;
  str[23]=0;
  if(x==0)
    print("0");
  while(x>0)
  {
    str[i] = (char)((x%10)+48);
    i--;
    x = x/10;
  }
  print(str+i+1);
}


void print_speed(const char *primitive, const unsigned int bytes, const unsigned long long *t, unsigned int tlen)
{
  unsigned int i;
  print(primitive);
  print(": ");
  if(bytes != (unsigned int)-1)
  {
    print("[");
    printllu(bytes);
    print("] ");
  }

  for(i=0;i<tlen-1;i++)
  {
    printllu(t[i+1]-t[i]);
    print(" ");
  }
  print("\n");
}


void print_stack(const char *primitive, const unsigned int bytes, unsigned int stack)
{
  print(primitive);
  print(": ");
  if(bytes != (unsigned int)-1)
  {
    print("[");
    printllu(bytes);
    print("] ");
  }

  printllu(stack);
    print(" stack bytes\n");
}
