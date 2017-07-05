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
print('#include "cpucycles.h"')
print('')
print('#define NRUNS 10')
print('')
print('int main(void)')
print('{')
print('  unsigned char st[48];')
print('  unsigned int i;')
print('  unsigned long long t[NRUNS];')
print('')

x = [(i * i * i + i * 0x9e3779b9) % (2 ** 32) for i in range(12)]
gen_arrays(x)

print('')
print('  print("array initialized !\\n");')
print('')
print('  for(i=0;i<NRUNS;i++)')
print('  {')
print('    t[i] = cpucycles();')
print('  }')
print('  print_speed("nothing",-1,t,NRUNS);')
print('')
print('  for(i=0;i<NRUNS;i++)')
print('  {')
print('    t[i] = cpucycles();')
print('    gimli(st);')
print('  }')
print('  print_speed("gimli",-1,t,NRUNS);')
print('')
print('  avr_end();')
print('  return 0;')
print('}')
