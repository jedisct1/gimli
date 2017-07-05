#include <stdlib.h>
#include "../api_hash.h"
#include "print.h"
#include "avr.h"
#include "fail.h"
#include "cpucycles.h"
#include <stdint.h>
#include <string.h>

#define NRUNS 5

int main(void)
{
  unsigned int i;
  unsigned long long t[NRUNS];

  uint8_t string1[] = "There's plenty for the both of us, may the best Dwarf win.";
  uint8_t string2[] = "If anyone was to ask for my opinion, which I note they're not, I'd say we were taking the long way around.";
  uint8_t string3[] = "Speak words we can all understand!";
  uint8_t string4[] = "It's true you don't see many Dwarf-women. And in fact, they are so alike in voice and appearance, that they are often mistaken for Dwarf-men.  And this in turn has given rise to the belief that there are no Dwarf-women, and that Dwarves just spring out of holes in the ground! Which is, of course, ridiculous.";
  uint8_t string5[] = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwx";
  uint8_t output[32];

  print("array initialized !\n");


  for(i=0;i<NRUNS;i++)
  {
    t[i] = cpucycles();
    Gimli_hash(string1, strlen( (const char *)string1), output, 32);
  }
  print_speed("gimli",-1,t,NRUNS);

  for(i=0;i<NRUNS;i++)
  {
    t[i] = cpucycles();
    Gimli_hash(string2, strlen( (const char *)string2), output, 32);
  }
  print_speed("gimli",-1,t,NRUNS);

  for(i=0;i<NRUNS;i++)
  {
    t[i] = cpucycles();
    Gimli_hash(string3, strlen( (const char *)string3), output, 32);
  }
  print_speed("gimli",-1,t,NRUNS);

  for(i=0;i<NRUNS;i++)
  {
    t[i] = cpucycles();
    Gimli_hash(string4, strlen( (const char *)string4), output, 32);
  }
  print_speed("gimli",-1,t,NRUNS);

  for(i=0;i<NRUNS;i++)
  {
    t[i] = cpucycles();
    Gimli_hash(string5, strlen( (const char *)string5), output, 32);
  }
  print_speed("gimli",-1,t,NRUNS);

  avr_end();
  return 0;
}
