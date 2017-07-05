#!/usr/bin/env python3

cycles = 0
inner_cycles = 0
file = 'gimli.s'

cycles_count = {
	'LDM' : 7,
	'MOV' : 1,
	'MOVS': 1,
	'PUSH': 2,
	'POP' : 2,
	'LSLS': 1,
	'ADDS': 1,
	'ANDS': 1,
	'EORS': 1,
	'ORRS': 1,
	'RORS': 1,
	'SUBS': 1,
	'STM' : 2,
}

with open(file, "r") as f:
	content = f.read().splitlines()

	for line in content:
		line = line.strip()
		if line and line.startswith('# START CYCLE COUNT'):
			inner_cycles = 0
		if line and line.startswith('# STOP CYCLE COUNT'):
			print('expected number of inner cycles:', inner_cycles)
		elif line and not line.startswith('#'):
			instr = line[0:4].strip()
			if instr in cycles_count:
				cycles += cycles_count[instr]
				inner_cycles += cycles_count[instr]

print('expected number of cycles:', cycles)

# print('test test')