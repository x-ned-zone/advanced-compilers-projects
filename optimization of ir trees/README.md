## Optimization of IR Trees

A program that applies constant folding and loop unrolling compiler optimisations to IR trees. 
The IR tree language is similar to that used in the Appel textbook. 

> Program reads in an IR tree and performs appropriate transformations (aggressively) to simplify the following subtrees wherever encountered:
```
op [CONST [x], CONST [y]]
SEQ[ SEQ[ SEQ[ SEQ[ SEQ[ SEQ[ SEQ[ SEQ[
                                        MOVE[TEMP[t1],CONST[x]],
                                        MOVE[TEMP[t2],CONST[y]]
                                    ],
                                    LABEL[start]
                            ],
                            CJUMP[<,TEMP[t1],TEMP[t2],NAME[t],NAME[f]]
                        ],
                        LABEL[f]
                    ],
                    loop_body
                ],
                MOVE[TEMP[t1],+[TEMP[t1],CONST[increment]]]
            ],
            JUMP[NAME[start]]
    ],
    LABEL[t]
]
```
... where op is one of +, -, *, /


In this IR language, the shorthand notation is used for all binary operators instead of BINOP and the CJUMP node has a standard format (as indicated above), with the op always being LT.

- For the loop unrolling, the entire structure is checked before replacing it with a simpler version.
- In the programs' replacement tree, the index variable is assigned first (t1 in the tree above) to a constant value before including a copy of the unrolled loop body. 

> The program's code handles any combination of these optimisations:
- multiple loop unrolls
- multiple constant folds, 
- some of each, etc.

> Input / Output:
- The program accepts a single command-line parameter that is the name of a data file containing the tree structure, 
with leading “=” symbols on each line to denote the nesting of child elements. 
- The program output is in the same format and is written to standard output (screen).

I devised my own algorithm convert(input and output) flat structure tree representation entails to list object.
- Algorithm implemented and is easy to understand from the code on 'generete AST'.

Further code improvement and developments were halted but can be done anytime later.