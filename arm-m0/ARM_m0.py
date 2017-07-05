#!/usr/bin/env python3


################################################
#
# ARM m0 instruction set for ease of use in python
#
################################################


#######################################
# register conversion

def r(idx):
	return 'r'+str(idx)

#######################################
# 32 bit instruction set

def MOV(rd,rr):
	print('MOV '+r(rd)+', '+r(rr))

def MOVI(rd,c):
	print('MOV '+r(rd)+', #'+str(c))

def require_low(rd):
	if rd > 7:
		comment('; incorect rd: '+ r(rd))

def require_lows(rd,rr):
	if rd > 7:
		comment('; incorect rd: '+ r(rd))
	if rr > 7:
		comment('; incorect rr: '+ r(rd))

def ADD(rd,c):
	require_low(rd)
	print('ADDS '+r(rd) +', #'+str(c))

def SUB(rd,c):
	require_low(rd)
	print('SUBS '+r(rd) +', #'+str(c))

def EOR(rd,rr):
	require_lows(rd,rr)
	print('EORS '+r(rd)+', '+r(rr))

def AND(rd,rr):
	require_lows(rd,rr)
	print('ANDS '+r(rd)+', '+r(rr))

def OR(rd,rr):
	require_lows(rd,rr)
	print('ORRS  '+r(rd)+', '+r(rr))

def LSL(rd,c):
	require_low(rd)
	print('LSLS '+r(rd) +', #'+str(c))

def MOVLSL(rd,rr,c):
	require_low(rd)
	print('LSLS '+r(rd) +', '+r(rr) +', #'+str(c))

def ROR(rd,rr):
	require_low(rd)
	require_low(rr)
	print('RORS '+r(rd)+', '+r(rr))

def PUSH(rd):
	print('PUSH {'+r(rd)+'}')

def POP(rd):
	print('POP {'+r(rd)+'}')

def LDMR(rd,ri,re):
	require_low(rd)
	require_low(ri)
	require_low(re)
	if(rd != ri):
		print('LDM  ' +r(rd)+ '!, {' +r(ri)+ ' - ' +r(re)+ '}')
	else:
		print('LDM  ' +r(rd)+ ', {' +r(ri)+ ' - ' +r(re)+ '}')

def STM(ra,rf):
	require_lows(ra,rf)
	if(ra != rf):
		print('STM  ' +r(ra)+ '!, {' +r(rf)+ '}')
	else:
		comment('unpredictable : '+r(ra)+ ', {' +r(rf)+ '}')


def STMR(rd,ri,re):
	require_low(rd)
	require_low(ri)
	require_low(re)
	if(rd != ri):
		print('STM  ' +r(rd)+ '!, {' +r(ri)+ ' - ' +r(re)+ '}')
	else:
		comment('unpredictable : '+r(rd)+ ', {' +r(ri)+ ' - ' +r(re)+ '}')

def LDI(rd, immediate):
	print('MOVS '+r(rd) + ', #'+ str(immediate))

#######################################

def push_to_stack():
	print('PUSH {r0-r7,lr}')
	MOV(1,8)
	MOV(2,9)
	MOV(3,10)
	MOV(4,11)
	MOV(5,12)
	MOV(6,14)
	print('PUSH {r1-r6}')

def pull_from_stack():
	print('POP {r1-r6}')
	MOV(8,1)
	MOV(9,2)
	MOV(10,3)
	MOV(11,4)
	MOV(12,5)
	MOV(14,6)
	print('POP {r0-r7,pc}')
	print('bx	lr')

def comment(string):
	if string == "":
		print("#")
	else:
		print("# " + string)