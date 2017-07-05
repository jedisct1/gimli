#!/usr/bin/env python3

import AVR

def init_state():
	return [[x, x+1, x+2, x+3] for x in range(0,24,4)]

def init_working():
	return [x + 24 for x in range(4)], [x + 28 for x in range(4)]

def small_swap(reg):
	reg[0], reg[3] = reg[3], reg[0]
	return reg

def spbox(idx,reg, t0, t1):
	x = reg[idx]
	y = reg[idx+1]
	z = reg[idx+2]
	AVR.comment('START SPBOX')
	AVR.comment('rotate x by 16: register renaming')
	# AVR.CLR0(t0)
	# AVR.ROL32(x,t0)
	# AVR.ROL32(x,t0)
	AVR.rotate8(x) # rotate by 8
	AVR.rotate8(x) # rotate by 8
	AVR.rotate8(x) # rotate by 8
	# 24 + 2 = 26
	AVR.comment('rotate y by 9 : 1 + register renaming')
	AVR.CLR0(t0)
	AVR.ROL32(y,t0)
	AVR.rotate8(y) # rotate by 8
	# 8 + 1 = 9
	AVR.comment('compute x')
	AVR.MOVW32(t1,x)
	AVR.MOVW32(t0,z)
	AVR.LSL32(t0)
	AVR.MOVW32(x,y)
	AVR.AND32(x,z)
	AVR.LSL32(x)
	AVR.LSL32(x)
	AVR.EOR32(x,t0)
	AVR.EOR32(x,t1)
	AVR.comment('compute y')
	AVR.MOVW32(t0,y)
	AVR.MOVW32(y,t1)
	AVR.OR32(y,z)
	AVR.LSL32(y)
	AVR.EOR32(y,t1)
	AVR.EOR32(y,t0)
	AVR.comment('compute z')
	AVR.AND32(t1,t0)
	AVR.LSL32(t1)
	AVR.LSL32(t1)
	AVR.LSL32(t1)
	AVR.EOR32(t0,t1)
	AVR.EOR32(z,t0)
	reg[idx], reg[idx+2] = reg[idx+2], reg[idx]
	AVR.comment('END SPBOX')
	return reg


def half_state_4SPbox(reg,round_value):
	# we need an additional register because we can't work on r28 r29 r30 r31
	wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
	reg = spbox(0,reg,wk_reg,wk_reg2)

	wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
	reg = spbox(0,reg,wk_reg,wk_reg2)

	wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
	reg = spbox(3,reg,wk_reg,wk_reg2)

	wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
	reg = spbox(3,reg,wk_reg,wk_reg2)

	reg = small_swap(reg)

	if round_value != 0 :
		AVR.LDI32(wk_reg,round_value)		# load into the third register
		AVR.EOR32(reg[0],wk_reg)		# xor only the third register

	wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
	reg = spbox(3,reg,wk_reg,wk_reg2)

	wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
	reg = spbox(3,reg,wk_reg,wk_reg2)

	wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
	reg = spbox(0,reg,wk_reg,wk_reg2)

	wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
	reg = spbox(0,reg,wk_reg,wk_reg2)

	return reg

def first_3SPboxes(reg,round_value):
	# we need an additional register because we can't work on r28 r29 r30 r31
	wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
	reg = spbox(0,reg,wk_reg,wk_reg2)

	wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
	reg = spbox(3,reg,wk_reg,wk_reg2)

	reg = small_swap(reg)

	if round_value != 0 :
		AVR.LDI32(wk_reg,round_value)		# load into the third register
		AVR.EOR32(reg[0],wk_reg)			# xor only the third register

	wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
	reg = spbox(3,reg,wk_reg,wk_reg2)

	wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
	reg = spbox(3,reg,wk_reg,wk_reg2)

	wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
	reg = spbox(0,reg,wk_reg,wk_reg2)

	wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
	reg = spbox(0,reg,wk_reg,wk_reg2)

	return reg

def last_SPboxes(reg):
	wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
	reg = spbox(0,reg,wk_reg,wk_reg2) # work on the first is done.

	wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
	reg = spbox(3,reg,wk_reg,wk_reg2) # work on the second is done

	return reg






def stack_load_left_to_right(reg):
	AVR.POPZ()				# idx + 48
	AVR.PUSH32(reg[3])
	AVR.PUSH32(reg[0])
	# DO WE DO ONLY  A SIMPLE REINIT OR A FULL ???
	reg[0].sort()						# we only re init the values in r[0] and r[3]
	reg[3].sort()						# we only re init the values in r[0] and r[3]
	AVR.SBIW(30,48)						# go the begining of the state
	AVR.LDZ32(reg[0])					# load r[0]
	AVR.LDZ32(reg[3])					# load r[3]
	AVR.ADIW(30,40)						# go back to idx+48 : 4 + 4 + 16 + 16
	AVR.PUSHZ()							# push to the stack : idx + 48
	return reg

def store_load_right_to_left(reg):
	AVR.POPZ()				# idx + 48
	AVR.STZ32(reg[5])		# store z
	AVR.STZ32(reg[2])		# store y
	AVR.SBIW(30,8)
	AVR.STZ32(reg[4])		# store x
	AVR.STZ32(reg[1])		# store z
	AVR.SBIW(30,8)
	AVR.STZ32(reg[3])		# store y
	AVR.STZ32(reg[0])		# store x
	reg = init_state()		# reinit the state.
	# current idx is +8
	AVR.ADIW(30,8)			# go to idx + 16
	AVR.LDZ32(reg[1])		# load r[1]
	AVR.LDZ32(reg[4])		# load r[2]
	AVR.ADIW(30,8)			# skip the next 4 words as they contain garbage (former r[3])
	AVR.LDZ32(reg[2])		# load r[4]
	AVR.LDZ32(reg[5])		# load r[5]
	# pop the initial values of the other half from the stack ! :p

	AVR.POP32(reg[0])		# load r[0]
	AVR.POP32(reg[3])		# load r[1]
	# current value of idx is +40
	AVR.PUSHZ()
	return reg

def stack_load_right_to_left(reg):
	AVR.POPZ()				# idx + 40
	AVR.PUSH32(reg[3])
	AVR.PUSH32(reg[0])
	reg[3].sort()
	reg[0].sort()
	# reg = reinit_state(reg)			# we only re init the values in r[0] and r[3]
	AVR.SBIW(30,32)						# skip the next two words
	AVR.LDZ32(reg[0])					# load r[0]
	AVR.LDZ32(reg[3])					# load r[3]
	AVR.ADIW(30,24)						# skip back 8 + 16
	# current value of idx is +40
	AVR.PUSHZ()
	return reg

def store_load_left_to_right(reg):
	AVR.POPZ()				# idx + 40
	AVR.STZ32(reg[5])		# store z
	AVR.STZ32(reg[2])		# store y
	AVR.SBIW(30,8)
	AVR.STZ32(reg[4])		# store x
	AVR.STZ32(reg[1])		# store z
	AVR.SBIW(30,8)
	AVR.STZ32(reg[3])		# store y
	AVR.STZ32(reg[0])		# store x
	reg = init_state()		# reinit the state.
	# current idx is 0
	AVR.ADIW(30,24)			# go to idx + 12 + 8
	AVR.LDZ32(reg[1])		# load r[1]
	AVR.LDZ32(reg[4])		# load r[2]
	AVR.ADIW(30,8)			# skip the next 8 words
	AVR.LDZ32(reg[2])		# load r[4]
	AVR.LDZ32(reg[5])		# load r[5]
	# pop the initial values of the other half from the stack ! :p
	AVR.POP32(reg[0])		# load r[0]
	AVR.POP32(reg[3])		# load r[1]
	# current value of idx is +48
	AVR.PUSHZ()
	return reg




def load(reg):
	# load the first column
	# load x then y then z
	reg = init_state()
	AVR.LDZ32(reg[0])
	AVR.LDZ32(reg[3])
	AVR.ADIW(30,8)
	AVR.LDZ32(reg[1])
	AVR.LDZ32(reg[4])
	AVR.ADIW(30,8)
	AVR.LDZ32(reg[2])
	AVR.LDZ32(reg[5])
	AVR.PUSHZ()						# save current pointer (point to the first half of the state)
	return reg

def store(reg):
	AVR.POPZ()
	AVR.STZ32(reg[5])		# store z
	AVR.STZ32(reg[2])		# store y
	AVR.SBIW(30,8)
	AVR.STZ32(reg[4])		# store x
	AVR.STZ32(reg[1])		# store z
	AVR.SBIW(30,8)
	AVR.STZ32(reg[3])		# store y
	AVR.STZ32(reg[0])		# store x
	return reg


print('.global avr_gimli')
print('.type avr_gimli, @function')
print('')
AVR.comment('*********************************************************')
AVR.comment(' avr_gimli')
AVR.comment(' apply the SPbox on 3 32 bit integers')
AVR.comment('')
AVR.comment(' Inputs:')
AVR.comment(' x      in register R25:R24')
AVR.comment('')
print('avr_gimli:')
print('')
AVR.comment('  state has the following form :')
AVR.comment('')
AVR.comment('  First row:')
AVR.comment('  00 01 02 03')
AVR.comment('  04 05 06 07')
AVR.comment('  08 09 10 11')
AVR.comment('  12 13 14 15')
AVR.comment('')
AVR.comment('  Second row:')
AVR.comment('  16 17 18 19')
AVR.comment('  20 21 22 23')
AVR.comment('  24 25 26 27')
AVR.comment('  28 29 30 31')
AVR.comment('')
AVR.comment('  Third row:')
AVR.comment('  32 33 34 35')
AVR.comment('  36 37 38 39')
AVR.comment('  40 41 42 43')
AVR.comment('  44 45 46 47')
AVR.comment('  */')

AVR.comment(' X,Y,Z: Indirect Address Register (X=R27:R26, Y=R29:R28, and Z=R31:R30)')
AVR.push_to_stack()
AVR.comment('START CYCLE COUNT')
constants = [0x9e377900 ^ (24 - 4 * x) for x in range(6)]




AVR.MOVW(30,24)								# load operand address state to Z
registers = init_state()

registers = load(registers)
registers = first_3SPboxes(registers,constants[0])		# rounds 1 2 3 - left
registers = store(registers)

AVR.ADIW(30,8)
registers = load(registers)
registers = first_3SPboxes(registers,0)					# rounds 1 2 3 - right
AVR.comment('last half is active, we did 3 rounds')
# idx = 24

# to minimize load and store, we push the current r[0] and r[3] to the stack
# load from the memory r[0] r[3] this is the big swap

registers = stack_load_left_to_right(registers)
# idx = 48

registers = half_state_4SPbox(registers,0)				# rounds 4 5 6 7 - right

# idx = 24
registers = store_load_right_to_left(registers)
# AVR.SBIW(30,24)								# idx = 0
# idx = 24

registers = half_state_4SPbox(registers,constants[1])	# rounds 4 5 6 7 - left
# first half is active, we did 7 rounds.
AVR.comment('first half is active, we did 7 rounds')

# idx = 0
registers = stack_load_right_to_left(registers)
# idx = 24

registers = half_state_4SPbox(registers,constants[2])	# rounds 8 9 10 11 - left

# idx = 0
registers = store_load_left_to_right(registers)
# AVR.ADIW(30,24)								# idx = 24
# idx = 48

registers = half_state_4SPbox(registers,0)				# rounds 8 9 10 11 - right
# last half is active, we did 11 rounds
AVR.comment('last half is active, we did 11 rounds')
# idx = 24




# to minimize load and store, we push the current head of r[0] and r[3] to the stack
# load from the memory r[0] r[3] this is the big swap

registers = stack_load_left_to_right(registers)
# idx = 48

registers = half_state_4SPbox(registers,0)				# rounds 12 13 14 15 - right

# idx = 24
registers = store_load_right_to_left(registers)
# AVR.SBIW(30,24)								# idx = 0
# idx = 24

registers = half_state_4SPbox(registers,constants[3])	# rounds 12 13 14 15 - left
# first half is active, we did 7 rounds.
AVR.comment('first half is active, we did 15 rounds')

# idx = 0
registers = stack_load_right_to_left(registers)
# idx = 24

registers = half_state_4SPbox(registers,constants[4])	# rounds 16 17 18 19 - left

# idx = 0
registers = store_load_left_to_right(registers)
# AVR.ADIW(30,24)								# idx = 24
# idx = 48

registers = half_state_4SPbox(registers,0)				# rounds 16 17 18 19 - right
# last half is active, we did 11 rounds
AVR.comment('last half is active, we did 19 rounds')
# idx = 24



# to minimize load and store, we push the current head of r[0] and r[3] to the stack
# load from the memory r[0] r[3] this is the big swap

registers = stack_load_left_to_right(registers)
# idx = 48

registers = half_state_4SPbox(registers,0)				# rounds 20 21 22 23 - right

# idx = 24
registers = store_load_right_to_left(registers)
# AVR.SBIW(30,24)								# idx = 0
# idx = 24

registers = half_state_4SPbox(registers,constants[5])	# rounds 20 21 22 23 - left
# first half is active, we did 7 rounds.
AVR.comment('first half is active, we did 23 rounds')


# idx = 0
registers = stack_load_right_to_left(registers)
# idx = 24

registers = last_SPboxes(registers)

# idx = 0
registers = store_load_left_to_right(registers)
# AVR.ADIW(30,24)								# idx = 0
# idx = 48

registers = last_SPboxes(registers)

registers = store(registers)

AVR.SBIW(30,8)

AVR.MOVW(24,30)							# back to its position
AVR.comment('STOP CYCLE COUNT')
AVR.pull_from_stack()