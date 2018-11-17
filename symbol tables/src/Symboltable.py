#Compilers 2 - semantic analysis - Symboltable
#author: Masixole Max Ntshinga

from HashTable import HashTable
import copy

# PROGRAM FEATURES
# beginscope: if outermost scope push OR else copy current hash_table array into stack
# endscope: pop top hash_table array from stack
# define: store variables in hashtable array which is stored in stack
# use:  access variables from HashTable array in stack

# UPDATES
# 1. DO NOT STORE/COPY whole HashTable into stack but only hash_array, and
#    access hashtable from Symboltable class for CRUD operations

class Symboltable:
    def __init__ (self, filename, tb_size):
        self.filename = filename
        self.stack = []
        self.arr_hash = [None] * tb_size
        self.hash_table = HashTable(tb_size)

    def push(self, value):
        self.stack.append(value)
    def peek(self):
        return self.stack[ len(self.stack)-1 ]
    def pop(self):
        return self.stack.pop()
    def isEmpty(self):
        return len(self.stack) == 0

    def runSymbolTable(self):
        try:
            f_program = open (self.filename, "r+")

            for f_line in f_program:
                line = f_line.strip()
                if line == "beginscope":
                    # create array part of hashtable and put in stack
                    if len(self.stack) == 0:
                        self.push(self.arr_hash)
                    else:
                        newHashTable = copy.deepcopy(self.peek())
                        self.push(newHashTable)
                    print(line)

                elif line.startswith("define"): # define 'name' 'value'
                    # put variable "name" + "value" in hashtable
                    key   = line.split()[1]
                    value = line.split()[2]
                    # self.peek().put(key, value)
                    self.hash_table.put(key, value, self.peek())
                    print(line)

                elif line.startswith("use"): # use 'name'
                    variable   = line.split()[1]
                    # on current stack position, find variable in HashTable
                    if self.isEmpty():
                        print(line + " = undefined")
                    else:
                        # found = self.peek().find(variable)
                        found = self.hash_table.find(variable, self.peek())
                        if found:
                            print(line + " = " + found)
                        else:
                            print(line + " = undefined")
                elif line == "endscope":
                    # remove current position from stack
                    self.pop()
                    print(line)
            f_program.close()

        except Exception as exp:
            print (exp.__str__())
