#!/usr/bin/python3

R = 24
S = 9

ror_r = 32 - R
ror_s = 32 - S

def enter():
    print(".syntax unified")
    print(".cpu cortex-m4")
    print("")
    print(".global gimli")
    print(".type gimli, %function")
    print("gimli:")
    print("    # Remember the ABI: we must not destroy the values in r4 to r15.")
    print("    # Arguments are placed in r0 and r1, the return value should go in r0.")
    print("    # To be certain, we just push all of them onto the stack.")
    print("    push {r4-r12,r14}")

def loadstate(state):
    print("    push {r0} // push the address to the stack")
    print("    mov r12, r0")
    print("ldm r12, {", end='', flush=True)
    for i in range(11):
        print(state[i]+",", end='', flush=True)
    print(state[11]+"}")


def leave():
    print("    # Finally, we restore the callee-saved register values and branch back.")
    print("    pop {r4-r12,r14}")
    print("    bx lr")

def storestate(state,tmp):
    print("    pop {"+tmp[0]+"} // pop the address from the stack")
    # XXX: :SOMEWHAT UGLY, swap tmp[0] and state[7] to have state regs in order for stm
    print("eor "+tmp[0]+", "+tmp[0]+", "+state[7])
    print("eor "+state[7]+", "+state[7]+", "+tmp[0])
    print("eor "+tmp[0]+", "+tmp[0]+", "+state[7])
    t = state[7]
    state[7] = tmp[0]
    tmp[0] = t

    print("stm "+tmp[0]+", {", end='', flush=True)
    for i in range(11):
        print(state[i]+",", end='', flush=True)
    print(state[11]+"}")


def bigswap(state):
    t = state[0]
    state[0] = state[2]
    state[2] = t
    t = state[1]
    state[1] = state[3]
    state[3] = t

def smallswap(state):
    t = state[0]
    state[0] = state[1]
    state[1] = t
    t = state[2]
    state[2] = state[3]
    state[3] = t

def spboxes(state,tmp):
    spbox(state, 0, tmp)
    spbox(state, 1, tmp)
    spbox(state, 2, tmp)
    spbox(state, 3, tmp)

def spbox(state, clmn, tmp):
    print("ror "+state[clmn]+", "+state[clmn]+", "+str(ror_r)) #XXX: get rid of this one
    print("eor "+tmp[0]+", "+state[clmn]+", "+state[clmn+8]+", lsl 1")
    print("and "+tmp[1]+", "+state[clmn+8]+", "+state[clmn+4]+", ror "+str(ror_s))
    print("eor "+tmp[0]+", "+tmp[0]+", "+tmp[1]+", lsl 2")

    print("orr "+tmp[1]+", "+state[clmn]+", "+state[clmn+8]+"")
    print("eor "+tmp[1]+", "+state[clmn]+", "+tmp[1]+", lsl 1")
    print("eor "+tmp[1]+", "+tmp[1]+", "+state[clmn+4]+", ror "+str(ror_s))

    print("and "+state[clmn]+", "+state[clmn]+", "+state[clmn+4]+", ror "+str(ror_s))
    print("eor "+state[clmn]+", "+state[clmn+8]+", "+state[clmn]+", lsl 3")
    print("eor "+state[clmn]+", "+state[clmn]+", "+state[clmn+4]+", ror "+str(ror_s))

    t = tmp[0]
    tmp[0] = state[clmn+8]
    state[clmn+8] = t

    t = tmp[1]
    tmp[1] = state[clmn+4]
    state[clmn+4] = t

state = ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11"]
tmp   = ["r12","r14"]

enter()
loadstate(state)

i = 24

print("    # round "+str(24))
spboxes(state,tmp)
smallswap(state)
print("    movw "+tmp[0]+", #"+str(0x7900 ^ 24))
print("    movt "+tmp[0]+", #0x9e37")
print("    eor "+state[0]+", "+state[0]+", "+tmp[0])
print("    # round "+str(i-1))
spboxes(state,tmp)
print("    # round "+str(i-2))
spboxes(state,tmp)
bigswap(state)
print("    # round "+str(i-3))
spboxes(state,tmp)

for i in reversed(range(4,21,4)):
    print("    # round "+str(i))
    spboxes(state,tmp)
    smallswap(state)
    print("    movw "+tmp[0]+", #"+str(0x7900 ^ i))
    print("    movt "+tmp[0]+", #0x9e37")
    print("    eor "+state[0]+", "+state[0]+", "+tmp[0])
    print("    # round "+str(i-1))
    spboxes(state,tmp)
    print("    # round "+str(i-2))
    spboxes(state,tmp)
    bigswap(state)
    print("    # round "+str(i-3))
    spboxes(state,tmp)

storestate(state,tmp)
leave()
