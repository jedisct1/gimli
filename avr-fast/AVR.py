#!/usr/bin/env python3


################################################
#
# AVR instruction set for ease of use in python
#
################################################


#######################################
# register conversion

def r(idx):
	return 'r'+str(idx)

#######################################
# 8 bit instruction set

def MOVW(rd,rr):
	print('MOVW '+r(rd)+', '+r(rr))

def MOV(rd,rr):
	print('MOV '+r(rd)+', '+r(rr))

def ADC(rd,rr):
	print('ADC '+r(rd)+', '+r(rr))

def EOR(rd,rr):
	print('EOR '+r(rd)+', '+r(rr))

def AND(rd,rr):
	print('AND '+r(rd)+', '+r(rr))

def OR(rd,rr):
	print('OR  '+r(rd)+', '+r(rr))

def LSL(rd):
	print('LSL '+r(rd))

def ROL(rd):
	print('ROL '+r(rd))

def PUSH(rd):
	print('PUSH '+r(rd))

def POP(rd):
	print('POP '+r(rd))

def LDZ(rd):
	print('LD  '+r(rd)+', Z+')

def STZ(rd):
	print('ST  -Z, '+r(rd))

def SBIW(rd,v):
	print('SBIW '+r(rd)+', '+str(v))

def SUBI(rd,v):
	print('SUBI '+r(rd)+', '+str(v))

def ADIW(rd,v):
	print('ADIW '+r(rd)+', '+str(v))

def ADDI(rd,v):
	# ADDI does not exist but the trick is to use the substraction by the oposite
	print('SUBI '+r(rd)+', -'+str(v))

def CLR(rd):
	print('CLR '+r(rd))

def CLR0(rd):
	print('CLR '+r(rd[0]))

def CLC():
	print('CLC')

def LDI(rd, immediate):
	print('LDI '+r(rd) + ', '+ str(immediate & 0xFF))

#######################################
# 32 bit instruction set

def EOR32(rd,rr):
	EOR(rd[0],rr[0])
	EOR(rd[1],rr[1])
	EOR(rd[2],rr[2])
	EOR(rd[3],rr[3])

def AND32(rd,rr):
	AND(rd[0],rr[0])
	AND(rd[1],rr[1])
	AND(rd[2],rr[2])
	AND(rd[3],rr[3])

def OR32(rd,rr):
	OR(rd[0],rr[0])
	OR(rd[1],rr[1])
	OR(rd[2],rr[2])
	OR(rd[3],rr[3])

def LSL32(rd):
	LSL(rd[3])
	ROL(rd[2])
	ROL(rd[1])
	ROL(rd[0])
	CLC()

def LDI32(rd, immediate):
	LDI(rd[0],immediate>>24)
	LDI(rd[1],immediate>>16)
	LDI(rd[2],immediate>>8)
	LDI(rd[3],immediate)

def LDI0_32(rd, immediate):
	CLR(rd[0])
	CLR(rd[1])
	CLR(rd[2])
	LDI(rd[3],immediate)

def CLR32(rd):
	CLR(rd[3])
	CLR(rd[2])
	CLR(rd[1])
	CLR(rd[0])

def ROL32(rd,t):
	LSL(rd[3])
	ROL(rd[2])
	ROL(rd[1])
	ROL(rd[0])
	ADC(rd[3],t[0])

def rotate8(reg):
	reg[0], reg[1], reg[2], reg[3] = reg[1], reg[2], reg[3], reg[0]
	return reg

def LDZ32(rd):
	LDZ(rd[0])
	LDZ(rd[1])
	LDZ(rd[2])
	LDZ(rd[3])

def STZ32(rr):
	STZ(rr[3])
	STZ(rr[2])
	STZ(rr[1])
	STZ(rr[0])

def PUSH32(rr):
	PUSH(rr[0])
	PUSH(rr[1])
	PUSH(rr[2])
	PUSH(rr[3])

def POP32(rd):
	# reverse order!
	POP(rd[3])
	POP(rd[2])
	POP(rd[1])
	POP(rd[0])

def PUSHZ():
	PUSH(30)
	PUSH(31)

def POPZ():
	POP(31)
	POP(30)

def mov_even(rd,rr):
	return (rd & 1 == 0) and (rr & 1 == 0)

def MOVW32(rd,rr):
	if 	mov_even(rd[0],rr[0]) and \
		  mov_even(rd[2],rr[2]) and \
		  rr[0] + 1 == rr[1] and \
		  rr[2] + 1 == rr[3]:
		MOVW(rd[0],rr[0])
		MOVW(rd[2],rr[2])
	else:
		comment("check MOVW")
		MOV(rd[0],rr[0])
		MOV(rd[1],rr[1])
		MOV(rd[2],rr[2])
		MOV(rd[3],rr[3])

def push_to_stack():
	for x in range(32):
		PUSH(x)
	print('')

def pull_from_stack():
	for x in range(32):
		POP(31-x)
	print('RET')

def comment(string):
	if string == "":
		print(";")
	else:
		print("; " + string)