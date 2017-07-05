#!/usr/bin/env python3

def gen_arrays(lst,arr):
	for i in range(12):
		for j in range(4):
			print('  '+arr+'['+str(4*i+j)+'] = 0x'+ hex((lst[i] >> (8*(3-j))) & 0xFF)[2:].zfill(2) + ';')

print('#include <stdlib.h>')
print('#include "../api.h"')
print('#include "print.h"')
print('#include "avr.h"')
print('#include "fail.h"')
print('')
print('void print_val(unsigned char v)')
print('{')
for j in range(256):
	print('if (v == ' + hex(j) +') print("' + hex(j)[2:].zfill(2) +'");')
print('}')
print('')
print('void print_state(unsigned char* v)')
print('{')
print('  int i;')
print('  for(i = 0; i < 48; ++i)')
print('  {')
print('    print_val(v[i]);')
print('    if (i % 4 == 3) print(" ");')
print('    if (i % 16 == 15) print("\\n");')
print('  }')
print('}')
print('')
print('int main(void)')
print('{')
print('  unsigned char st[48];')
# print('  unsigned char ex[48];')
print('')

x = [(i * i * i + i * 0x9e3779b9) % (2 ** 32) for i in range(12)]
gen_arrays(x,'st')
y = [0x8ef32cb5,0xcbfba0aa,0x345cf7e9,0xbcd314ef,0xe1da6e40,0xddf4b60f,0x58ebf147,0xd292fe55,0x74829a24,0xe1a3efa5,0xfa614031,0x3e7fb38d]

# without constant addition:
# y = [0x2e58f21f,0x67cf5816,0x411eccfd,0x5f823c1c,0x6d17471e,0xe7d58bda,0x2f638c59,0xb7b77f8b,0x5e7208da,0xb470d15b,0xf9f42f66,0xe6e3af7b]
# single SP-box
# y = [0x896628ec,0x284d2390,0x3900875c,0x0bc43f70,0x54f16937,0x99dea96d,0xff8d41eb,0xddc5d869,0x4084420e,0x9a7653b5,0xdbc061f6,0x49098fb6]
print('')
# gen_arrays(y,'ex')

print('')
print('  print("array initialized !\\n");')
print('')
print('  print("----------------------\\n");')
print('  print("initial state:\\n");')
print('  print("----------------------\\n");')
print('  print_state(st);')
print('  gimli(st);')
print('')
print('  print("----------------------\\n");')
print('  print_state(st);')
print('  print("----------------------\\n");')
# print('  print("target state:\\n");')
# print('  print("----------------------\\n");')
# print('  print_state(ex);')
# print('  print("----------------------\\n");')
print('')
print('  avr_end();')
print('  return 0;')
print('}')
