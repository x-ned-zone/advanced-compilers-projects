#!/usr/bin/python

#Compilers 2 - Optimization of IR Trees
#author: Masixole Max Ntshinga

import sys
from IROptimization import IROptimization

def main():
    if len(sys.argv)>=2:
        symb = IROptimization (sys.argv[1])
        symb.optimizeIR()
    else:
        print ("Error: filename argument missing!")
        print ("To run program, use the command e.g: 'python3 main.py test1.ir'")

if "__main__" == __name__:
  main()
