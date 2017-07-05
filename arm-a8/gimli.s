.arm
.fpu neon
.text

.align 4
.global _gimli
.global gimli


_gimli:
gimli:

mrc p15, 0, r2, c9, c13, 0

vldmia r0,{q0-q2} 

movw  r1, #:lower16:gimli_rot8
movt  r1, #:upper16:gimli_rot8

ldr r12,=6

vld1.8 d24,[r1]

movw  r1, #:lower16:gimli_rconsts
movt  r1, #:upper16:gimli_rconsts


looptop:



    vshr.u32 q15,q1,#23 // round 4; state is in q0,q1,q2
  vtbl.8 d0,{d0},d24 // round 4

    vshl.i32 q1,q1,#9 // round 4

vshl.i32 q10,q2,#1  // round 4: q10 = z << 1
  vtbl.8 d1,{d1},d24 // round 4

    veor q1,q1,q15 // round 4

vorr q9,q0,q2     // round 4: q9 = x|z

vand q8,q0,q1     // round 4: q8 = x&y

veor q5,q1,q2     // round 4: q5 = y^z

veor q6,q0,q1     // round 4: q6 = x^y

vshl.i32 q8,q8,#3 // round 4: q8 = (x&y)<<3
        vld1.8 {d22-d23},[r1,: 128]! // load round constant

vshl.i32 q9,q9,#1 // round 4: q9 = (x|z)<<1

veor q8,q8,q5     // round 4: q8 = y^z ^ ((x&y)<<3)

vand q3,q1,q2     // round 4: q3 = y&z

veor q9,q9,q6     // round 4: q9 = x^y ^ ((x|z)<<1)
      vrev64.i32 q8,q8 // round 4: Small-Swap

veor q10,q0,q10   // round 4: q10 = x^(z<<1)

vshl.i32 q3,q3,#2 // round 4: q3 = (y&z)<<2

        veor q8,q8,q11 // add round constant

veor q10,q10,q3   // round 4: q10 = x ^ (z << 1) ^ ((y&z)<<2)

    vshr.u32 q15,q9,#23 // round 3; state is in q8,q9,q10

  vtbl.8 d16,{d16},d24 // round 3

    vshl.i32 q9,q9,#9 // round 3

vshl.i32 q2,q10,#1  // round 3: q2 = z << 1
  vtbl.8 d17,{d17},d24 // round 3

    veor q9,q9,q15 // round 3

vorr q1,q8,q10     // round 3: q1 = x|z

vand q0,q8,q9     // round 3: q0 = x&y

veor q5,q9,q10     // round 3: q5 = y^z

veor q6,q8,q9     // round 3: q6 = x^y

vshl.i32 q0,q0,#3 // round 3: q0 = (x&y)<<3

vshl.i32 q1,q1,#1 // round 3: q1 = (x|z)<<1

veor q0,q0,q5     // round 3: q0 = y^z ^ ((x&y)<<3)

vand q3,q9,q10     // round 3: q3 = y&z

veor q1,q1,q6     // round 3: q1 = x^y ^ ((x|z)<<1)

veor q2,q8,q2   // round 3: q2 = x^(z<<1)
  vtbl.8 d0,{d0},d24 // round 2
vshl.i32 q3,q3,#2 // round 3: q3 = (y&z)<<2

    vshr.u32 q15,q1,#23 // round 2; state is in q0,q1,q2

veor q2,q2,q3   // round 3: q2 = x ^ (z << 1) ^ ((y&z)<<2)
  vtbl.8 d1,{d1},d24 // round 2

    vshl.i32 q1,q1,#9 // round 2

vshl.i32 q10,q2,#1  // round 2: q10 = z << 1

    veor q1,q1,q15 // round 2

vorr q9,q0,q2     // round 2: q9 = x|z

vand q8,q0,q1     // round 2: q8 = x&y

veor q5,q1,q2     // round 2: q5 = y^z

veor q6,q0,q1     // round 2: q6 = x^y

vshl.i32 q8,q8,#3 // round 2: q8 = (x&y)<<3

vshl.i32 q9,q9,#1 // round 2: q9 = (x|z)<<1

veor q8,q8,q5     // round 2: q8 = y^z ^ ((x&y)<<3)

vand q3,q1,q2     // round 2: q3 = y&z

veor q9,q9,q6     // round 2: q9 = x^y ^ ((x|z)<<1)

veor q10,q0,q10   // round 2: q10 = x^(z<<1)

vshl.i32 q3,q3,#2 // round 2: q3 = (y&z)<<2

    vshr.u32 q15,q9,#23 // round 1; state is in q8,q9,q10

veor q10,q10,q3   // round 2: q10 = x ^ (z << 1) ^ ((y&z)<<2)
  vtbl.8 d27,{d16},d24 // round 1

    vshl.i32 q9,q9,#9 // round 1

vshl.i32 q2,q10,#1  // round 1: q2 = z << 1
  vtbl.8 d26,{d17},d24 // round 1

    veor q9,q9,q15 // round 1

vorr q1,q13,q10     // round 1: q1 = x|z

vand q0,q13,q9     // round 1: q0 = x&y

          subs r12,r12,#1

veor q5,q9,q10     // round 1: q5 = y^z

veor q6,q13,q9     // round 1: q6 = x^y

vshl.i32 q0,q0,#3 // round 1: q0 = (x&y)<<3

vshl.i32 q1,q1,#1 // round 1: q1 = (x|z)<<1

veor q0,q0,q5     // round 1: q0 = y^z ^ ((x&y)<<3)

vand q3,q9,q10     // round 1: q3 = y&z

veor q1,q1,q6     // round 1: q1 = x^y ^ ((x|z)<<1)

veor q2,q13,q2   // round 1: q2 = x^(z<<1)

vshl.i32 q3,q3,#2 // round 1: q3 = (y&z)<<2


veor q2,q2,q3   // round 1: q2 = x ^ (z << 1) ^ ((y&z)<<2)


bne looptop

vstmia r0,{q0-q2}

mrc p15, 0, r3, c9, c13, 0

sub r0,r3,r2

bx lr
