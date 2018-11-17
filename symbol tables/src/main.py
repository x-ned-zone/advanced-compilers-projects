#!/usr/bin/python

#Compilers 2 - semantic analysis - Symboltable
#author: Masixole Max Ntshinga

import sys
from Symboltable import Symboltable

def main():
    if len(sys.argv)>=2:
        symb = Symboltable (sys.argv[1], tb_size = 5 )
        symb.runSymbolTable()
    else:
        print ("Error: filename argument missing!")
        print ("To run program, use the command e.g: 'python3 main.py test1.dat'")

if "__main__" == __name__:
  main()
