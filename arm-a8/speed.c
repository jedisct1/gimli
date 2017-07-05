#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define NRUNS 1001

int uint32_cmp(const void *a, const void *b) 
{ 
  const uint32_t *ia = (uint32_t *)a; 
  const uint32_t *ib = (uint32_t *)b;
  if (*ia > *ib) return 1;
  if (*ia < *ib) return -1; 
  return 0;
} 


extern unsigned long long cpucycles(void);

extern uint32_t gimli(uint32_t *state);

int main(void)
{
  int i;
  uint32_t t[NRUNS];
  uint32_t state[12];

  asm volatile("mcr p15, 0, %0, c9, c12, 0" :: "r"(17));
  asm volatile("mcr p15, 0, %0, c9, c12, 1" :: "r"(0x8000000f));
  asm volatile("mcr p15, 0, %0, c9, c12, 3" :: "r"(0x8000000f));

  printf("=== gimli benchmarks ===\n");
  for(i=0;i<NRUNS;i++)
  {
    printf("%u ", t[i] = gimli(state));
  }
  qsort(t, NRUNS, sizeof(uint32_t), uint32_cmp);
  printf("\nmedian:    %u\n", t[NRUNS/2]);

  return 0;
}
