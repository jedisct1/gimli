#include <stdio.h>

extern void gimli(unsigned int *);

int main()
{
  unsigned int x[24];
  int i;

  for (i = 0;i < 24;++i) x[i] = i * i * i + i * 0x9e3779b9;

  gimli(x);

  for (i = 0;i < 12;++i) {
    printf("%08x ",x[i]);
    if (i % 4 == 3) printf("\n");
  }

  for (i = 0;i < 24;++i) x[(i + 12) % 24] = i * i * i + i * 0x9e3779b9;

  gimli(x);

  for (i = 0;i < 12;++i) {
    printf("%08x ",x[i + 12]);
    if (i % 4 == 3) printf("\n");
  }
  return 0;
}
