#include <stdio.h>

extern void gimli(unsigned int *);

int main()
{
  unsigned int x[48];
  int pos;
  int i;

  for (pos = 0;pos < 48;pos += 12) {
    for (i = 0;i < 48;++i) x[(i + pos) % 48] = i * i * i + i * 0x9e3779b9;
  
    gimli(x);
  
    for (i = 0;i < 12;++i) {
      printf("%08x ",x[i + pos]);
      if (i % 4 == 3) printf("\n");
    }
  }

  return 0;
}
