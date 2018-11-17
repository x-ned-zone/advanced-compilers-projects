## Instruction Selection

A compilers phenomenon.
- Expresses a machine instruction as a fragment of an IR tree – "tree pattern"
- Instruction selection is equivalent to tiling the tree with a minimal set of tree patterns.

This program aims to:
- convert IR trees into simplified Python 2/3 (and generate machine code tiles)
- select instructions using the maximal munch algorithm. This is a simple example of a cross-compiler, using the same toolchain that is used to generate machine code.
- The goal is to develop a set of appropriate tiles for machine code and/or Python statements, similar to the Jouette architecture.

Assumptions: 
- All IR trees are error-free.

> Input / Output
- Program accepts a single command-line parameter that is the name of a data file containing the tree structure, with leading “=” symbols on each line to denote the nesting of child elements. 
- Program output is a sequence of Python instructions written to standard output (screen). 

In the example below, the IR tree gets an input value and adds 1 before outputting it, and the equivalent Python code is below it.

> Input (Flat structure IR tree):
  ```
  SEQ
  =MOVE
  ==MEM
  ===+
  ====TEMP
  =====FP
  ====CONST
  =====x
  ==CALL
  ===NAME
  ====input
  =CALL
  ==NAME
  ===print
  ==+
  ===MEM
  ====+
  =====TEMP
  ======FP
  =====CONST
  ======x
  ===CONST
  ====1
  ```

> Output (Python code)
  ```
  v0 = eval ( input () )
  x = v0
  v1 = x + 1
  print (v1)
  ```

The simplified Python 3 subset must include at least:
  ```
  variable = e
  variable
  print (e)
  x = eval (input ())
  e1 = e2 + e3
  e1 = e2 - e3
  e1 = e2 * e3
  e1 = e2 / e3
  if (e<1): s1 else: s2
  while (e<1): s1
  ```

> For each Python statement/IR tree, appropriate set of tiles is defined for matching. For example:

| Python/from IR | Tiles  | 
| ---------------|------------------------------------:|
| variable=e | MOVE[MEM[+[CONST variable, TEMP FP]], e]  MOVE[MEM[+[TEMP FP, CONST variable]], e]  |
| print (e)  | CALL[NAME[print],e] | 
| e1=e2+e3   | +[e2,e3]  | 
| e1=e2+c    | +[e2,CONST[c]] | 
| e1=c+e2    | +[CONST[c],e2] | 

> Programming language used: Python

> Scope guide:
- Accurate instruction generation for basic test cases. 30 pnts
- Appropriate tiles for language subset. 30 pnts
- Generation of matching variable names. 10 pnts
- Accurate operation and test cases for if. 10 pnts
- Accurate operation and test cases for while. 10 pnts
- Exhaustive testing / creativity. 10 pnts
