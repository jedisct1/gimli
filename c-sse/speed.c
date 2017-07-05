#include <stdio.h>
#include <unistd.h>

extern void gimli(unsigned int *);

long long cpucycles(void)
{
  unsigned long long result;
  asm volatile(".byte 15;.byte 49;shlq $32,%%rdx;orq %%rdx,%%rax"
    : "=a" (result) ::  "%rdx");
  return result;
}

int main()
{
  unsigned int x[12];
  int i;
  unsigned long long t[21];

  for (i = 0;i < 12;++i) x[i] = getpid() + i;

  for (i = 0;i < 21;++i) {
    t[i] = cpucycles();
  }

  for (i = 0;i < 21;++i) {
    t[i] = cpucycles();
    gimli(x);
    gimli(x);
    gimli(x);
    gimli(x);
    gimli(x);
    gimli(x);
    gimli(x);
    gimli(x);
    gimli(x);
    gimli(x);
  }

  for (i = 0;i < 20;++i) printf("%lld * 0.1\n",t[i + 1] - t[i]);
  return 0;
}
