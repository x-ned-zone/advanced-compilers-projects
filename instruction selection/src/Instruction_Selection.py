"""
Practical:
Compilers 2 : Instruction Selection
Date: 30-May-2018

Masixole M. Ntshinga

v1 submit - Used the order of if-elif statements to choose the maximum tile first and then process subtrees further
v2 submit - fixed while loop
v3 submit - COMPLETE 

"""

class Instruction_Selection:
    def __init__ (self, filename):
        self.filename = filename 
        self.ast_tree = [] 
        self.curr_children = []

        self.tiles = []
        self.instructions = []
        self.python3_cd = []
        
        # ... { 'value': 'variable', ... } 
        self.var_dict = {}
        self.r = [None]*32

    #======================================================================
    # Main entry
    #======================================================================
    def tile (self):
        arr = []
        try:
            f_program = open (self.filename, "r+") 
            
            for line in f_program:
                f_line = line.strip()
                if (f_line):
                    c_level = f_line.rfind("=")+1
                    c_line = f_line [c_level:]
                    self.ast_tree.append([c_level, c_line]) 

            f_program.close()
        except Exception as exp:
            print ("")
            print ("File not found! Check filename or file locaton.")
            print ("")
            print (exp.__str__())

        self.generate_ast()
        self.ast_tree = self.ast_tree[0][1:]

        self.maximalM(self.ast_tree)

        self.get_output()


    #============================================================================
    # GENERATE AST TREE
    #============================================================================
    # Convert a Flat Structure to a List-Tree
    # Iterative from the end of the list, adding children to next upper root node 
    def generate_ast(self):
        ir_code = self.ast_tree
        for i in range(len(ir_code)-1, -1, -1):
            node = ir_code[i]

            # Find children for this node in cached-children list with lower recent children
            for c in range (len(self.curr_children)-1,-1,-1):
                child = self.curr_children[c]
                if node[0]==child[0]-1:
                    node.append(child[1:])
                    self.curr_children.remove(child) # remove child from child list
            
            self.curr_children.append(node)
            
            # done with this node, remove it.
            if (i>0):
                ir_code[i]=None

    #======================================================================
    # RECURISIVE maximul munch
    # Tiles

    # 1. Start at the root.
    # 2. Find the largest tile that fits.
    # 3. Cover the root and possibly several other nodes with this tile.
    # 4. Repeat for each subtree.
    # 5. Generates self.instructions in reverse order.
    # 6. If two tiles of equal size match the current node, choose either.

    #======================================================================
    def maximalM(self, ir_tree):

        # print("ir_tree : ", ir_tree)
        r0 = "0"
        if (ir_tree[0] == "CALL"):  # [CALL, [name], []]

            if ( ir_tree[1][1][0] == "print"):
                name = ir_tree[1][1][0]
                value = self.maximalM( ir_tree[2] )
                
                self.tiles.append("CALL : (name : "+name+") , (--) ) ")
                
                if value in self.var_dict:
                    self.python3_cd.append( "" + name + " ("+self.var_dict[value]+")") 
                else:
                    self.python3_cd.append( "" + name + " ("+value+")") 

                if value in self.var_dict:
                    return name + " ("+self.var_dict[value]+")"
                else:
                    return name + " ("+value+")"

            # ASSIGN TO VARIABLE
            elif ( ir_tree[1][1][0] == "input"):
                return "eval ( input () )"

            else:
                print("CALL error")

        elif (ir_tree[0] == "SEQ"):


            # Sub-children index:
            S=0  # S (root)
            L=1  # L(left)
            R=2  # R(right)
            if ir_tree[R][0] == "LABEL" and ( ir_tree [L][0] == "SEQ" or ir_tree[L][R][0] == "JUMP"):
                # WHILE LOOP:
                # ===========
                if ir_tree [L][0] == "SEQ" and ir_tree[L][R][0] == "JUMP": 
                    if ir_tree [L][L][0] == "SEQ": 
                        if ir_tree [L][L][L][0] == "SEQ" and ir_tree[L][L][L][R][0] == "LABEL": 
                            if ir_tree [L][L][L][L][0] == "SEQ":
                                c_jump_st = ir_tree[L][L][L][L][R]  # = [CJUMP, e, LT, 1, done, body]
                                if c_jump_st[0]=="CJUMP" and ir_tree[L][L][L][L][L][0] == "LABEL":

                                    exp = self.maximalM (c_jump_st[1])
                                    cond_op = self.cond_op (c_jump_st[2][0])
                                    r_val = self.maximalM (c_jump_st[3])                                    
                                    s = self.maximalM(ir_tree[L][L][R])
                                    # While loop (python):
                                    
                                    # remove r_val & exp duplicates from py 
                                    if r_val in self.var_dict and exp in self.var_dict  :
                                        py = "while (" + self.var_dict[exp] +" "+ cond_op +" "+ self.var_dict[r_val] + "): " + s
                                    else:
                                        print("dict : ", self.var_dict)                                        
                                        py = "while (" + exp +" "+ cond_op +" "+ r_val + "): " + s

                                    if "" + s in self.python3_cd :
                                        self.python3_cd.remove("" + s) 

                                    self.python3_cd.append( py )

                                    self.tiles.append("SEQ : ( SEQ : (SEQ : (SEQ : (SEQ : LABEL, (CJUMP, (--), "+c_jump_st[2][0]+", (--),  LABEL, LABEL )), LABEL), (--)), JUMP:(NAME)),LABEL")
                                    
                                    return py
                # IF STATEMENT:
                # =============
                elif ir_tree[L][0] == "SEQ" :
                    if ir_tree[L][L][0] == "SEQ" and ir_tree[L][L][R][0] == "LABEL":
                        if ir_tree[L][L][L][0] == "SEQ" and ir_tree[1][1][1][2][0] == "JUMP":
                            if ir_tree[L][L][L][L][0] == "SEQ" :
                                if ir_tree[L][L][L][L][L][0] == "SEQ" and ir_tree[L][L][L][L][L][2][0] == "LABEL": 
                                    # Condition
                                    c_jump_st = ir_tree[L][L][L][L][L][L]    #  = [CJUMP, e, LT, 1, NAME t, NAME f]
                                    if c_jump_st[0] == "CJUMP" and self.evaluate (c_jump_st[1]) and c_jump_st[3][0] == "CONST" and c_jump_st[4][0] == "NAME" and c_jump_st[5][0] == "NAME":
                                        exp = self.maximalM(c_jump_st[1])
                                        cond_op = self.cond_op ( str(c_jump_st[2][0])) 
                                        r_val = self.maximalM(c_jump_st[3])
                                        s1 = self.maximalM(ir_tree[L][2])
                                        s2 = self.maximalM(ir_tree[L][L][L][L][2])

                                        # IF statement (python):
                                        if r_val in self.var_dict and exp in self.var_dict  :
                                            py = "if ( "+self.var_dict[exp]+" "+cond_op+" "+self.var_dict[r_val]+" ): "+s1+"    else: " + s2
                                        else:
                                            print("dict : ", self.var_dict)
                                            py = "if ( "+exp+" "+cond_op+" "+r_val+" ): "+s1+"    else: " + s2
                                      
                                        # remove s1 & s2 duplicates from py 
                                        if "" + s1 in self.python3_cd and "" + s2 in self.python3_cd:
                                            self.python3_cd.remove("" + s1) 
                                            self.python3_cd.remove("" + s2)

                                        self.python3_cd.append( py )
                                       
                                        self.tiles.append("SEQ : (SEQ : (SEQ : (SEQ : (SEQ : (SEQ : (CJUMP, (--), "+str(c_jump_st[2][0])+", (--), NAME, NAME,LABEL), (--)), JUMP ) , LABEL) , (--) ), LABEL)")
                                        return py

            else:
                # Execute remaining statements from first to all children
                for i in range(1, len(ir_tree)):                   
                    stm = self.maximalM( ir_tree[i] )
                    self.tiles.append("SEQ : (--), (--)")

        elif (ir_tree[0] == "ESEQ"):
            # evaluate s 
            s = self.maximalM( ir_tree[1] )
            # return e 
            e = self.maximalM( ir_tree[2] )
            self.tiles.append("ESEQ : (--), (--)")

            return e

        elif ir_tree[0] == "TEMP":
            ri = ir_tree[1][0]

            return ri

        # ADD I  [CONST: ]
        elif ir_tree[0] == "CONST":
            n = int(self.reg())
            self.r[n] = self.reg() 
            rg = self.r[n]
            
            ri = "r0" + " + " + ir_tree[1][0]
           
            # create variable 
            if ri not in self.var_dict:
                self.var_dict[ ri ] = "v"+str(len(self.var_dict))   

            # add python code
            self.python3_cd.append( self.var_dict[ ri ] + " = "+ ir_tree[1][0])  #r0 + " + " +

            self.instructions.append("ADDI  r"+rg+" <= "+ ri)
            self.tiles.append("CONST "+ ir_tree[1][0]) 

            return self.var_dict[ ri ]

        # Binary Op: [+ - / *] : node & node
        # "ri <= rj + rk"
        elif ir_tree[0] in ["+","-","/","*"] :
            tile = ""
            instr = ""
            ri=""
            c = ""

            # allocate register
            n = int(self.reg())
            self.r[n] = self.reg() 
            rg = self.r[n]

            #ADD I   [+  : CONST & node ]
            if ir_tree[0] == "+" and ir_tree[1][0]=="CONST" and self.isNode(ir_tree[2]):
                rj = self.maximalM(ir_tree[2]) 
                ri = rj + " + " + ir_tree[1][1][0]
                tile = "+ : CONST "+ ir_tree[1][1][0] +", (--)"
                instr = "ADDI  r"+rg+" <= "+ri
 
            #ADD I   [+  : node & CONST ]
            elif ir_tree[0] == "+" and self.isNode(ir_tree[1]) and ir_tree[2][0]=="CONST":
                rj = self.maximalM(ir_tree[1])
                ri = rj+ " + " + ir_tree[2][1][0]
                tile = "+ : (--), CONST "+ir_tree[2][1][0]+""
                instr = "ADDI  r"+rg+" <= "+ri 

            # SUBB I  [-  :  node & CONST ]
            elif ir_tree[0] == "-" and self.isNode(ir_tree[1]) and ir_tree[2][0]=="CONST":
                rj = self.maximalM(ir_tree[1]) 
                ri = rj + " - " + ir_tree[2][1][0]
                tile = "- : (--), CONST "+ir_tree[2][1][0]+""
                instr = "SUBBI  r"+rg+" <= "+ri  

            # ADD / MUL / SUB / DIV
            else:  
                rj = self.maximalM(ir_tree[1])
                rk = self.maximalM(ir_tree[2])
                ri = str(rj) +" "+ ir_tree[0] +" "+ str(rk)
                tile = ir_tree[0] + " : (--), (--)"
                
                if ir_tree[0] == "+":
                    instr = "ADD  r"+rg+" <= " + ri 
                elif ir_tree[0] == "-":
                    instr = "SUB  r"+rg+" <= " + ri 
                elif ir_tree[0] == "*":
                    instr = "MUL  r"+rg+" <= " + ri 
                elif ir_tree[0] == "/":
                    instr = "DIV  r"+rg+" <= " + ri 
            
            self.instructions.append(instr)
            self.tiles.append(tile)
            return ri

        # Load  =  [Mem : [+ : [CONST] & [node] ] ] 
        #        | [Mem : [+ : [node] & [CONST] ] 
        #        | [Mem : [CONST] ]
        #        | [Mem : [node]] ]
        # "ri <= M [ rj + c ]"
        elif ir_tree[0] == "MEM":
            ri = None
            tile = ""
            c = ""
            # allocate register
            n = int(self.reg())
            self.r[n] = self.reg() 
            rg = self.r[n]

            if ir_tree[1][0]=="+":
        
                if ir_tree[1][1][0]=="CONST" and self.isNode(ir_tree[1][2]) :
                    rj = self.maximalM(ir_tree[1][2])
                    ri = "M [ " + rj + " + " + ir_tree[1][1][1][0] +" ]"
                    tile = "MEM : (+ : (CONST "+ir_tree[1][1][1][0]+"), (--) )"
                    c = ir_tree[1][1][1][0]

                elif self.isNode(ir_tree[1][1])  and ir_tree[1][2][0]=="CONST":
                    rj = self.maximalM(ir_tree[1][1])
                    ri = "M [ " + rj + " + " + ir_tree[1][2][1][0]+" ]"
                    tile = "MEM : (+ : (--), CONST "+ir_tree[1][2][1][0]+")"
                    c = ir_tree[1][2][1][0]
 
            elif ir_tree[1][0]=="CONST" :
                ri = "M [ " + r0 + " + " + ir_tree[1][1][0]+" ]"
                tile ="MEM : (CONST "+ir_tree[1][1][0]+")"
                c = ir_tree[1][1][0]
       
            elif self.isNode(ir_tree[1]):
                rj = self.maximalM(ir_tree[1])
                ri = "M [ " + rj + " + " + r0 +" ]"
                tile ="MEM : (--)"
                c = rj
            
            # load variable
            # add python code
            if ri in self.var_dict:
                self.var_dict[ri] =  c 
                self.python3_cd.append(self.var_dict[ri]  + " = " + c)
            else:
                self.var_dict[ri] =  "v"+str(len(self.var_dict))  
                self.python3_cd.append(self.var_dict[ri] + " = " +  c)

            # add instruction
            self.instructions.append("LOAD  r"+rg+" <= " + ri) 
            
            # add tile
            self.tiles.append(tile)

            return self.var_dict[ri]

        # MoveM  =   [Move : (Mem: node ) & (Mem: node ) ]
        elif ir_tree[0] == "Move" and (ir_tree[1][0]=="MEM" and self.isNode(ir_tree[1][1]) ) \
                                  and (ir_tree[2][0]=="MEM" and self.isNode(ir_tree[2][1]) ): 
            rj=self.maximalM(ir_tree[1][1]) 
            ri=self.maximalM(ir_tree[2][1]) 
            M = "M [ " + rj + "] <= M [ " + ri + "]"

            # create variable
            # ... if already exists, update it, or 
            if ri in self.var_dict:
                if rj in  self.var_dict:
                    self.python3_cd.append(self.var_dict[rj] + " = " + self.var_dict[ri])
                    self.var_dict[ri] = rj 
                else:
                    self.python3_cd.append(rj + " = " + self.var_dict[ri])
            else:
                if rj in self.var_dict:
                    self.python3_cd.append( self.var_dict[rj]  + " = " + ri)
                    self.var_dict[ri] = rj 
                else:
                    self.python3_cd.append(rj + " = " + ri)
 
            # add instruction
            self.instructions.append( "MoveM  " + M )            
            
            # add tile
            self.tiles.append("Move : (MEM,  MEM)")            

            return "MoveM  " + M 

        # Store =  [MOVE:  [MEM:  [+: [CONST] & [node]]  ] & [node] ]
        #        | [MOVE:  [MEM:  [+: [node]  & [CONST]] ] & [node] ]
        #        | [MOVE:  [MEM:  [CONST]] & node] ]
        #        | [MOVE:  [MEM:  [node]]] & [node] ]
        elif ir_tree[0] == "MOVE": 

            rj, ri, c = None, None, None
            tile = ""
            instr = ""
            if ir_tree[1][0]=="MEM" and self.isNode(ir_tree[2]):  
           
                if ir_tree[1][1][0]=="+":

                    if ir_tree[1][1][1][0]=="CONST" and self.isNode(ir_tree[1][1][2]):
                        rj=self.maximalM(ir_tree[1][1][2])
                        ri=self.maximalM(ir_tree[2])
                        c = ir_tree[1][1][1][1][0]
                        tile = "MOVE : (MEM : (+ : (CONST " + c + ", (--)) ) ), (--)"
               
                    elif self.isNode(ir_tree[1][1][1])  and ir_tree[1][1][2][0]=="CONST":
                        rj=self.maximalM(ir_tree[1][1][1])
                        ri=self.maximalM(ir_tree[2])
                        c = ir_tree[1][1][2][1][0]
                        tile = "MOVE : (MEM : (+ : ((--), CONST "+c+") ) ), (--)"
                
                elif ir_tree[1][1][0]=="CONST":
                    ri=self.maximalM(ir_tree[2])
                    rj=0
                    c = ir_tree[1][1][1][0]
                    tile = "MOVE : (MEM : (CONST "+c+")), (--)"

                elif self.isNode(ir_tree[1][1]):
                    rj=self.maximalM(ir_tree[1][1])
                    ri=self.maximalM(ir_tree[2])
                    c = 0
                    tile = "MOVE : (MEM : ((--)), (--)"

                instr = "M [ "+rj+" + "+c+" ] <= "+ri

                if not c == 0:
                    # create variable (if new)
                    self.var_dict[ri] = c
                else:
                    pass

                # add python code
                # create variable (if new) 
                if ri in self.var_dict:
                    self.python3_cd.append( c + " = " + ri )
                else:
                    self.python3_cd.append( c + " = " + self.var_dict[ri] )

                # add instruction
                self.instructions.append( "STORE  " + instr )

                # add tile
                self.tiles.append(tile)

            return instr
 
        else:
            print( "----: ", ir_tree) 

    # ========================================================================================================
    # Auxiliary functions
    def evaluate(self, t_node):
         return t_node[0] in ["MEM","+", "-", "/", "*","TEMP","CONST"]

    def isNode(self, t_node): 
        return t_node[0] in ["CALL", "MEM", "MOVE", "JUMP", "CJUMP", "ESEQ", "SEQ", "CALL", "+", "-", "/", "*","TEMP"] 

    def testing(self, ir_tree):
        pass

    def cond_op(self,op):
        opr = ""
        if op=="LT": 
            opr="<"
        elif op=="GT": 
            opr=">"
        elif op=="NE": 
            opr="not ="
        elif op=="EQ":
            opr="=" 
        return opr

    #find free register
    def reg(self):
        for i in range(1,33):
            if self.r[i]==None:
                return str(i)

    def get_output(self):
        print("=======================================")
        print("IR Code in Tree: \n")
        print(self.ast_tree)

        print("\nMaximal Munch")
        print("=======================================")
        print("Instructions:")
        
        try: 
            out_inst = open (self.filename[:self.filename.index(".")]+".out_instr", "w+") 

            c = 0
            for inst in self.instructions:
                c += 1
                print()
                print(str(c) + ".  " + inst)
                out_inst.write(inst)
                out_inst.write("\n")
            out_inst.close()
        except Exception as exp:
            print ("Instr output error : " + exp.__str__())

        print("\n=======================================")
        print("Tiles:")

        try:
            x = 0
            out_tile = open (self.filename[:self.filename.index(".")]+".tiles", "w+") 
            for tile in (self.tiles):
                x +=1
                print()
                print(str(x)+".  "+tile)
                out_tile.write(tile)
                out_tile.write("\n")
            out_tile.close()
        except Exception as exp:
            print ("Tiles output error : "+exp.__str__())

        print("\n=======================================")
        print("Python 3 (code):\n")
        try:
            out_program = open (self.filename[:self.filename.index(".")]+".out_py", "w+") 
            for p in (self.python3_cd):
                print(p)
                out_program.write(p)
                out_program.write("\n")
            out_program.close()
        except Exception as exp:
            print ("Python output error : "+exp.__str__())

        print("=======================================") 
