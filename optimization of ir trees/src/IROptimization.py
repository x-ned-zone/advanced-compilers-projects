
class IROptimization:
    def __init__ (self, filename):
        self.filename = filename
        self.roots = []
        self.ast_tree = []

    def push(self, value):
        self.roots.append(value)
    def peek(self):
        return self.roots[ len(self.roots)-1 ]
    def pop(self):
        return self.roots.pop()
    def isEmpty(self):
        return len(self.roots) == 0

    #========================================================================================================================================================
    # main entry
    #========================================================================================================================================================
    def optimizeIR(self):
        try:
            f_program = open (self.filename, "r+")
            root = 0
            self.push(root)
            for f_line in f_program:
                line = f_line.strip()
                c_level = line.rfind("=")+1
                c_line = line[c_level:]
                self.ast_tree.append(line)
                # self.generate_tree(root, c_line, c_level)

            f_program.close()

        except Exception as exp:
            print (exp.__str__())

        self.constantUnfold(self.ast_tree)
        self.loopUnroll(self.ast_tree)
        # print("roots :", self.roots)
        # print("ast   :", self.ast_tree)

        for n in self.ast_tree:
            if n:
                print(n)
    #========================================================================================================================================================
    # GENERATE AST TREE
    #========================================================================================================================================================
    def generate_tree(self, root, data, level):
        # root
        root = self.peek()

        if level == 0:
            self.nodeInsert(level, self.ast_tree, data, 0)

        # new subtree, new-root level
        elif level > root:
            self.push(level)
            self.nodeInsert(level, self.ast_tree, data, 0)

        # back to previous-root level
        elif level < root:
            last_level = root

            while( last_level > level ):
                self.pop()
                # print("pop:", self.pop())
                last_level -= 1

            self.push(level)
            self.nodeInsert(level, self.ast_tree, data, 0)

    #========================================================================================================================================================
    # RECURISIVE NODE Insert
    #========================================================================================================================================================

    def nodeInsert(self, alevel, aTree, data, index):

        alevel = self.roots[index]
        if index == len(self.roots)-1:
            if len(aTree)==0:
                aTree.append(data)
            else:
                aTree.append([data])

        elif alevel < len(aTree):
            index +=1
            # alevel = self.roots[index]
            if alevel==0:
                self.nodeInsert(alevel, aTree, data, index)
            else:
                self.nodeInsert(alevel, aTree[alevel], data, index)

        else:
            pass
    #========================================================================================================================================================
    # CONSTANT UNFOLDING
    #========================================================================================================================================================
    def constantUnfold(self, prog_code):
        for i in range(len(prog_code)-1 , 0, -1):
            aline = prog_code[i]

            if aline:
                c_line = aline[ aline.rfind("=")+1 :]
                if c_line == "+":
                    if prog_code[i+1] [ prog_code[i+1].rfind("=")+1 :] == "CONST":
                        new_value = int(prog_code[i+2] [ prog_code[i+2].rfind("=")+1 :]) + int(prog_code[i+4] [prog_code[i+2].rfind("=")+1 :])
                        prog_code[i]="="*(aline.rfind("=")+1)+"CONST"
                        prog_code[i+1]="="*(prog_code[i+1].rfind("=")+1)+str(new_value)
                        self.nullify(i, prog_code)

                elif c_line == "-":
                    if prog_code[i+1] [ prog_code[i+1].rfind("=")+1 :] == "CONST":
                        new_value = int(prog_code[i+2] [ prog_code[i+2].rfind("=")+1 :]) - int(prog_code[i+4] [ prog_code[i+2].rfind("=")+1 :])
                        prog_code[i]="="*(aline.rfind("=")+1)+"CONST"
                        prog_code[i+1]="="*(prog_code[i+1].rfind("=")+1)+str(new_value)
                        self.nullify(i, prog_code)

                elif c_line == "/":
                    if prog_code[i+1] [ prog_code[i+1].rfind("=")+1 :] == "CONST":
                        new_value = int(int(prog_code[i+2] [ prog_code[i+2].rfind("=")+1 :]) / int(prog_code[i+4] [ prog_code[i+2].rfind("=")+1 :]) )
                        prog_code[i]="="*(aline.rfind("=")+1)+"CONST"
                        prog_code[i+1]="="*(prog_code[i+1].rfind("=")+1)+str(new_value)
                        self.nullify(i, prog_code)

                elif c_line == "*":
                    if prog_code[i+1] [ prog_code[i+1].rfind("=")+1 :] == "CONST":
                        new_value = int(prog_code[i+2] [ prog_code[i+2].rfind("=")+1 :]) * int(prog_code[i+4] [ prog_code[i+2].rfind("=")+1 :])
                        prog_code[i]="="*(aline.rfind("=")+1)+"CONST"
                        prog_code[i+1]="="*(prog_code[i+1].rfind("=")+1)+str(new_value)
                        self.nullify(i, prog_code)

        return prog_code

    def nullify(self, i, prog_code):
        del prog_code[i+4]
        del prog_code[i+3]
        del prog_code[i+2]
    #========================================================================================================================================================
    # LOOP UNROLLING
    #========================================================================================================================================================
    def loopUnroll(self, prog_code):
        pass
