
import sys
from Instruction_Selection import Instruction_Selection

def main():
    if len(sys.argv)>=2:
        symb = Instruction_Selection (sys.argv[1])
        symb.tile()
    else:
        print ("Error: filename argument missing!")
        print ("To run program, use the command e.g: 'python3 main.py test1.ir'")

if "__main__" == __name__:
  main()