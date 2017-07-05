#!/usr/bin/env python3

import AVR

def init_state():
	return [[x, x+1, x+2, x+3] for x in range(0,24,4)]

def init_working():
	return [x + 24 for x in range(4)], [x + 28 for x in range(4)]

def big_swap():
	reg = init_state()
	AVR.LDZ32(reg[0])
	AVR.LDZ32(reg[1])
	AVR.LDZ32(reg[2])
	AVR.LDZ32(reg[3])
	AVR.STZ32(reg[1])
	AVR.STZ32(reg[0])
	AVR.STZ32(reg[3])
	AVR.STZ32(reg[2])

def spbox(idx,reg, t0, t1):
	x = reg[idx]
	y = reg[idx+1]
	z = reg[idx+2]
	AVR.comment('START SPBOX')
	AVR.comment('rotate x by 16: no register renaming')
	AVR.PUSH(x[0])
	AVR.MOV(x[0],x[3])
	AVR.MOV(x[3],x[2])
	AVR.MOV(x[2],x[1])
	AVR.POP(x[1])

	# 24 + 2 = 26
	AVR.comment('rotate y by 9 : 1 + register renaming')

	AVR.CLR0(t0)
	AVR.ROL32(y,t0)
	AVR.PUSH(y[0])
	AVR.MOV(y[0],y[1])
	AVR.MOV(y[1],y[2])
	AVR.MOV(y[2],y[3])
	AVR.POP(y[3])

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

	AVR.comment('swap x and z')
	AVR.PUSH32(z)
	AVR.MOV(z[0],x[0])
	AVR.MOV(z[1],x[1])
	AVR.MOV(z[2],x[2])
	AVR.MOV(z[3],x[3])
	AVR.POP32(x)
	return reg

def load():
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

def store():
	reg = init_state()
	AVR.STZ32(reg[5])		# store z
	AVR.STZ32(reg[2])		# store y
	AVR.SBIW(30,8)
	AVR.STZ32(reg[4])		# store x
	AVR.STZ32(reg[1])		# store z
	AVR.SBIW(30,8)
	AVR.STZ32(reg[3])		# store y
	AVR.STZ32(reg[0])		# store x


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

AVR.MOVW(30,24)								# load operand address state to Z

AVR.LDI(28,24)
AVR.LBL('roundf')
AVR.CPI(28,0)
AVR.BREQ('jroundfend')
AVR.JMP('hop')
AVR.LBL('jroundfend')
AVR.JMP('end')
AVR.LBL('hop')
AVR.PUSH(28)

# apply the SBox

AVR.LBL('spboxes')
AVR.LDI(28,2)

AVR.LBL('spbx')
AVR.CPI(28,0)
AVR.BREQ('jspbxend')

AVR.JMP('hopspx')
AVR.LBL('jspbxend')
AVR.JMP('spbxend')
AVR.LBL('hopspx')
AVR.PUSH(28)

load()
AVR.PUSHZ()

AVR.JMP('spbox')
AVR.LBL('spboxend')

AVR.POPZ()
store()
AVR.ADIW(30,8)

AVR.POP(28)
AVR.DEC(28)
AVR.JMP('spbx')
AVR.LBL('spbxend')

AVR.SBIW(30,16)

# pop the constant of the round
AVR.POP(28)

AVR.LDI(27,3)
AVR.AND(27,28)
AVR.CPI(27,0)

AVR.BRNE('bigswap')

reg = init_state()
AVR.LDZ32(reg[0])
AVR.LDZ32(reg[1])
AVR.LDZ32(reg[2])
AVR.LDZ32(reg[3])
AVR.STZ32(reg[2])
AVR.STZ32(reg[3])
AVR.STZ32(reg[0])

# ROUND CONSTANT
AVR.LDI(24,0x9e)
AVR.LDI(25,0x37)
AVR.LDI(26,0x79)

AVR.EOR(reg[1][0],24)
AVR.EOR(reg[1][1],25)
AVR.EOR(reg[1][2],26)
AVR.EOR(reg[1][3],28)

AVR.STZ32(reg[1])

AVR.DEC(28)
AVR.JMP('roundf')

AVR.LBL('bigswap')
AVR.CPI(27,2)
AVR.BRNE('endloop')

# if  BIG SWAP
big_swap()

AVR.LBL('endloop')

AVR.DEC(28)
AVR.JMP('roundf')


#####################################################################################################
#
# SPBOX COMPUTATION : THE LOADED HALF

AVR.LBL('spbox')
AVR.LDI(29,2)

AVR.LBL('sps')
AVR.CPI(29,0)
AVR.BREQ('jspsend')

AVR.JMP('hopsp')
AVR.LBL('jspsend')
AVR.JMP('spsend')
AVR.LBL('hopsp')

AVR.PUSH(29)

reg = init_state()
wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
reg = spbox(0,reg,wk_reg,wk_reg2)

wk_reg, wk_reg2 = init_working()						# additional registers used for computation : r24 - r31
# this is not optimal. But whatever...
AVR.MOVW32(wk_reg,reg[0])
AVR.MOVW32(reg[0],reg[3])
AVR.MOVW32(reg[3],wk_reg)

AVR.MOVW32(wk_reg,reg[1])
AVR.MOVW32(reg[1],reg[4])
AVR.MOVW32(reg[4],wk_reg)

AVR.MOVW32(wk_reg,reg[2])
AVR.MOVW32(reg[2],reg[5])
AVR.MOVW32(reg[5],wk_reg)

AVR.POP(29)
AVR.DEC(29)
AVR.JMP('sps')
AVR.LBL('spsend')

AVR.JMP('spboxend')

#####################################################################################################

AVR.LBL('end')
AVR.MOVW(24,30)							# back to its position
AVR.comment('STOP CYCLE COUNT')
AVR.pull_from_stack()