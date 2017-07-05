#!/usr/bin/env python3

import Gimli

x = [(i * i * i + i * 0x9e3779b9) % (2 ** 32) for i in range(12)]

x = [[x[4 * i + j] for i in range(3)] for j in range(4)]

Gimli.print_to_hex(x)
x = Gimli.gimli(x)
Gimli.print_to_hex(x)
