#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
print(sys.argv[1])
cpu = CPU()

program = sys.argv[1]
cpu.load(program)

cpu.run()