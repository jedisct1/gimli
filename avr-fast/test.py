#!/usr/bin/env python3

cycles = 0
inner_cycles = 0
file = 'gimli.s'

cycles_count = {
	'MOVW' : 1,
	'MOV' : 1,
	'ADC' : 1,
	'EOR' : 1,
	'AND' : 1,
	'OR' : 1,
	'LSL' : 1,
	'ROL' : 1,
	'PUSH' : 2,
	'POP' : 2,
	'LD' : 2,
	'ST' : 2,
	'SBIW' : 2,
	'SUBI' : 1,
	'ADIW' : 2,
	'CLR' : 1,
	'CLC' : 1,
	'LDI' : 1
}




with open(file, "r") as f:
	content = f.read().splitlines()

	for line in content:
		line = line.strip()
		if line and line.startswith('; START CYCLE COUNT'):
			inner_cycles = 0
		if line and line.startswith('; STOP CYCLE COUNT'):
			print('expected number of inner cycles:', inner_cycles)
		elif line and not line.startswith(';'):
			instr = line[0:4].strip()
			if instr in cycles_count:
				cycles += cycles_count[instr]
				inner_cycles += cycles_count[instr]

print('expected number of cycles:', cycles)

# print('test test')