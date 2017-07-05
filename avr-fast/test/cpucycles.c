#include "cpucycles.h"
#include <avr/io.h>
#include <avr/interrupt.h>

static unsigned long long ticks;
static unsigned char init = 0;

static void cpucycles_init(void)
{
  ticks = 0;
#if defined (__AVR_ATmega128__)
  TCCR1B = (1 << CS12); // Set up timer 
  TIMSK |= (1 << TOIE1);
#else
  TCCR0B = (1 << CS00); // Set up timer 
  TCCR1B = (1 << CS12); // Set up timer 
  TIMSK1 |= (1 << TOIE1);
#endif	
  TCNT0 = 0;
  TCNT1 = 0;
  sei(); // Enable global interrupts
  init = 1;
}

// Interrupt handler, called automatically on
// TIMER1 overflow
ISR(TIMER1_OVF_vect)
{
  ticks += (1UL << 24);
}

unsigned long long cpucycles(void)
{
  if(!init)
    cpucycles_init();
  unsigned long long rh = TCNT1;
  unsigned long long rl = TCNT0;
  return ticks | (rh << 8) | rl; 
}


