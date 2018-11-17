#Compilers 2 - semantic analysis - Symboltable
#author: Masixole Max Ntshinga

from Node import Node

class HashTable:
    def __init__(self, size_):
        # Create a new empty hash table and an array of size_ for the hash keys
        self.tb_size = size_
        # self.arr_hash = [None] * size_

    def hashfunction(self, s_key, tablesize_arg):
         hashIndex = 0
         temp = 0

         for i in range (0, len(s_key)):
            # Convert string (key) into equivalent natural number
            temp = 1 * (temp + int(s_key[i], 36))  # radix-37 notation

         # compute index in hash table
         hashIndex = temp % tablesize_arg
         return hashIndex

    def put(self, key, value, array_hash):
        i = self.hashfunction(key, self.tb_size)
        # self.arr_hash [i] = Node (key, value, self.arr_hash [i])
        array_hash [i] = Node (key, value, array_hash [i])

    def get(self,key, array_hash):
        if not self.isEmpty(array_hash):
            # return self.arr_hash[key]
            return array_hash[key]
        else:
            return None

    def find(self, name, array_hash):
        #use hash function for new element
        value = None
        for i in range(0, self.tb_size ):
            # ht_index = self.arr_hash[i]
            ht_index = array_hash[i]

            while ht_index != None:
                if ht_index.variable == name:
                    value = ht_index.value
                    break
                else:
                    ht_index = ht_index.next
        return value

    def isEmpty(self, array_hash):
        # return len(self.arr_hash) == 0
        return len(array_hash) == 0
