#!/usr/bin/env python3

R = 24
S = 9

ror_r = 32 - R
ror_s = 32 - S

import ARM_m0

def small_swap(reg):
	ARM_m0.comment('SMALL SWAP')
	reg[0], reg[1] = reg[1], reg[0]
	return reg

def permute(current_active,inactive):
	ARM_m0.comment('START SWAP ACTIVE BLOCK')
	ARM_m0.MOV(7,current_active[0]);
	# current_active[0] is now at position 7
	ARM_m0.MOV(current_active[0],inactive[0]);
	ARM_m0.MOV(inactive[0],current_active[1]);

	ARM_m0.MOV(current_active[1],inactive[1]);
	ARM_m0.MOV(inactive[1],current_active[2]);

	ARM_m0.MOV(current_active[2],inactive[2]);
	ARM_m0.MOV(inactive[2],current_active[3]);

	ARM_m0.MOV(current_active[3],inactive[3]);
	ARM_m0.MOV(inactive[3],current_active[4]);

	ARM_m0.MOV(current_active[4],inactive[4]);
	ARM_m0.MOV(inactive[4],current_active[5]);

	ARM_m0.MOV(current_active[5],inactive[5]);
	ARM_m0.MOV(inactive[5],7);

	previous_active = list(current_active)
	previous_inactive = list(inactive)

	inactive[0] = previous_active[0]
	inactive[1] = previous_active[1]
	inactive[2] = previous_active[2]
	inactive[3] = previous_active[3]
	inactive[4] = previous_active[4]
	inactive[5] = previous_active[5]

	current_active[1] = previous_inactive[0]
	current_active[2] = previous_inactive[1]
	current_active[3] = previous_inactive[2]
	current_active[4] = previous_inactive[3]
	current_active[5] = previous_inactive[4]
	current_active[0] = previous_inactive[5]
	ARM_m0.comment('END SWAP ACTIVE BLOCK')
	return current_active, inactive

def big_swap(current_active,inactive):
	ARM_m0.comment('START BIG SWAP')

	ARM_m0.MOV(7,current_active[0]);
	# current_active[0] is now at position 7
	ARM_m0.MOV(current_active[0],inactive[0]);
	ARM_m0.MOV(inactive[0],current_active[1]);

	ARM_m0.MOV(current_active[1],inactive[1]);
	ARM_m0.MOV(inactive[1],7);

	inactive[0], inactive[1] = inactive[1], inactive[0]

	ARM_m0.comment('END BIG SWAP')
	return current_active, inactive

def big_swap_permute(current_active,inactive):
	ARM_m0.comment('START SWAP ACTIVE BLOCK')
	ARM_m0.MOV(7,current_active[2]);

	ARM_m0.MOV(current_active[2],inactive[2]);
	ARM_m0.MOV(inactive[2],current_active[3]);

	ARM_m0.MOV(current_active[3],inactive[3]);
	ARM_m0.MOV(inactive[3],current_active[4]);

	ARM_m0.MOV(current_active[4],inactive[4]);
	ARM_m0.MOV(inactive[4],current_active[5]);

	ARM_m0.MOV(current_active[5],inactive[5]);
	ARM_m0.MOV(inactive[5],7);

	previous_active = list(current_active)
	previous_inactive = list(inactive)

	inactive[0] = previous_active[0]
	inactive[1] = previous_active[1]
	inactive[2] = previous_active[2]
	inactive[3] = previous_active[3]
	inactive[4] = previous_active[4]
	inactive[5] = previous_active[5]

	current_active[0] = previous_inactive[0]
	current_active[1] = previous_inactive[1]
	current_active[2] = previous_inactive[5]
	current_active[3] = previous_inactive[2]
	current_active[4] = previous_inactive[3]
	current_active[5] = previous_inactive[4]
	ARM_m0.comment('END SWAP ACTIVE BLOCK')
	return current_active, inactive


def spbox(reg,idx, t0, t1):
	x = reg[idx]
	y = reg[idx + 2]
	z = reg[idx + 4]
	ARM_m0.comment('START SPBOX')
	ARM_m0.comment('rotate x <<< '+str(R))
	ARM_m0.LDI(t0,ror_r)
	ARM_m0.ROR(x,t0)
	ARM_m0.comment('rotate y  <<< '+str(S))
	ARM_m0.LDI(t0,ror_s)
	ARM_m0.ROR(y,t0)
	ARM_m0.comment('compute x')
	ARM_m0.MOV(t1,x)
	ARM_m0.MOV(t0,z)
	ARM_m0.LSL(t0,1)
	ARM_m0.MOV(x,y)
	ARM_m0.AND(x,z)
	ARM_m0.LSL(x,2)
	ARM_m0.EOR(x,t0)
	ARM_m0.EOR(x,t1)
	ARM_m0.comment('compute y')
	ARM_m0.MOV(t0,y)
	ARM_m0.MOV(y,t1)
	ARM_m0.OR(y,z)
	ARM_m0.LSL(y,1)
	ARM_m0.EOR(y,t1)
	ARM_m0.EOR(y,t0)
	ARM_m0.comment('compute z')
	ARM_m0.AND(t1,t0)
	ARM_m0.LSL(t1,3)
	ARM_m0.EOR(t0,t1)
	ARM_m0.EOR(z,t0)
	reg[idx], reg[idx + 4] = reg[idx + 4] , reg[idx]
	return reg

def load_cst(rt, rnd):
	ARM_m0.LDI(rt,0x9e)
	ARM_m0.LSL(rt,8)
	ARM_m0.ADD(rt,0x37)
	ARM_m0.LSL(rt,8)
	ARM_m0.ADD(rt,0x79)
	ARM_m0.LSL(rt,8)
	ARM_m0.ADD(rt,rnd)

print('.syntax unified')
print('.cpu cortex-m0')
print('.align 2')
print('    .global gimli')
print('    .type   gimli, %function')
print('.text')
print('gimli:')

ARM_m0.comment('*********************************************************')
ARM_m0.comment(' Inputs:')
ARM_m0.comment(' x      in register r0')
ARM_m0.comment('')

ARM_m0.push_to_stack()

ARM_m0.comment('START CYCLE COUNT')
ARM_m0.LDMR(0,1,6)
ARM_m0.MOV(8,1)
ARM_m0.MOV(9,2)
ARM_m0.MOV(10,3)
ARM_m0.MOV(11,4)
ARM_m0.MOV(12,5)
ARM_m0.MOV(14,6)
ARM_m0.LDMR(0,1,6)
ARM_m0.comment("pos - > reg")
ARM_m0.comment("0l   - >  8")
ARM_m0.comment("1l   - >  9")
ARM_m0.comment("2r   - >  10")
ARM_m0.comment("3r   - >  11")
ARM_m0.comment("4l   - >  12")
ARM_m0.comment("5l   - >  14")
ARM_m0.comment("6r   - >  1")
ARM_m0.comment("7r   - >  2")
ARM_m0.comment("8l   - >  3")
ARM_m0.comment("9l   - >  4")
ARM_m0.comment("10r  - >  5")
ARM_m0.comment("11r  - >  6")
ARM_m0.PUSH(0)
ARM_m0.MOV(0,3)
ARM_m0.MOV(3,10)
ARM_m0.MOV(10,4)
ARM_m0.MOV(4,11)
ARM_m0.MOV(11,0)

right = [3,4,1,2,5,6]
left = [8,9,12,14,11,10]

right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = small_swap(right)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)

right, left = permute(right,left)

left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = small_swap(left)
load_cst(0,24)
ARM_m0.EOR(left[0],0)
# add constants
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
# 3 rounds

left, right = big_swap(left,right)

left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = small_swap(left)
load_cst(0,20)
ARM_m0.EOR(left[0],0)
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)

left, right = permute(left,right)

right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = small_swap(right)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)

# 7 rounds

right, left   = big_swap_permute(right,left)

ARM_m0.comment("XXXXXX")
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = small_swap(left)
load_cst(0,16)
ARM_m0.EOR(left[0],0)
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)

left, right = permute(left,right)

right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = small_swap(right)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
# 11 rounds

right, left = big_swap_permute(right,left)

left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = small_swap(left)
load_cst(0,12)
ARM_m0.EOR(left[0],0)
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)

left, right = permute(left,right)

right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = small_swap(right)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
# 15rounds

right, left = big_swap_permute(right,left)

left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = small_swap(left)
load_cst(0,8)
ARM_m0.EOR(left[0],0)
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)

left, right = permute(left,right)

right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = small_swap(right)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
# 19 rounds

right, left = big_swap_permute(right,left)

left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = small_swap(left)
load_cst(0,4)
ARM_m0.EOR(left[0],0)
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)
left = spbox(left,0,0,7)
left = spbox(left,1,0,7)

left, right = permute(left,right)

right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = small_swap(right)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
right = spbox(right,0,0,7)
right = spbox(right,1,0,7)
# 23 rounds

right, left = big_swap_permute(right,left)

left = spbox(left,0,0,7)
left = spbox(left,1,0,7)

left, right = permute(left,right)

right = spbox(right,0,0,7)
right = spbox(right,1,0,7)

ARM_m0.POP(0)
ARM_m0.SUB(0,40)
ARM_m0.STM(0,right[0])
ARM_m0.STM(0,right[1])
ARM_m0.ADD(0,8)
ARM_m0.STM(0,right[2])
ARM_m0.STM(0,right[3])
ARM_m0.ADD(0,8)
ARM_m0.STM(0,right[4])
ARM_m0.STM(0,right[5])
right, left = permute(right,left)
ARM_m0.SUB(0,48)
ARM_m0.STM(0,left[0])
ARM_m0.STM(0,left[1])
ARM_m0.ADD(0,8)
ARM_m0.STM(0,left[2])
ARM_m0.STM(0,left[3])
ARM_m0.ADD(0,8)
ARM_m0.STM(0,left[4])
ARM_m0.STM(0,left[5])
ARM_m0.SUB(0,40)

ARM_m0.comment('STOP CYCLE COUNT')
ARM_m0.pull_from_stack()
