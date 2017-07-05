#!/usr/bin/env python3

def gen_arrays(lst):
	k = 3
	for j in range(48):
		if j % 4 == 0 :
			k = 3
		print('  st['+str(j)+'] = 0x'+ hex((lst[j>>2] >> (8*k)) & 0xFF)[2:].zfill(2) + ';')
		k -= 1;

print('#include <stdlib.h>')
print('#include "../api.h"')
print('#include "print.h"')
print('#include "avr.h"')
print('#include "fail.h"')
print('')
print('#define NRUNS 10')
print('')
print('unsigned char st[48];')
print('unsigned int i;')
print('unsigned int ctr=0,newctr;')
print('unsigned char canary;')
print('volatile unsigned char *p;')
print('extern unsigned char _end;')
print('extern unsigned char __stack;')
print('')
print('static unsigned int stack_count(unsigned char canary)')
print('{')
print('  const unsigned char *p = &_end;')
print('  unsigned int c = 0;')
print('  while(*p == canary && p <= &__stack)')
print('  {')
print('    p++;')
print('    c++;')
print('  }')
print('  return c;')
print('}')
print('')
print('#define WRITE_CANARY(X) {p=X;while(p>= &_end) *(p--) = canary;}')
print('')
print('int main(void)')
print('{')
print('')

x = [(i * i * i + i * 0x9e3779b9) % (2 ** 32) for i in range(12)]
gen_arrays(x)

print('  volatile unsigned char a; /* Mark the beginning of the stack */')
print('')
print('  for(i=0;i<NRUNS;i++)')
print('  {')
print('    canary = random();')
print('    WRITE_CANARY(&a);')
print('')
print('    gimli(st);')
print('    newctr =(unsigned int)&a - (unsigned int)&_end - stack_count(canary);')
print('    ctr = (newctr>ctr)?newctr:ctr;')
print('  }')
print('  print_stack("gimli ",-1,ctr);')
print('')
print('  avr_end();')
print('  return 0;')
print('}')
