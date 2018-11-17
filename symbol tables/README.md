## Symbol Tables

###Aims 
> To build a functional hash-table implementation of a Symbol Table to handle simple constant definitions and uses in a statically-scoped block structured language.
> Use a stack to maintain copies of hash table arrays for outer scopes. 
> Use a hash table array size of N=5, with chaining for collision resolution. 
> Use a reasonable hashing algorithm.

- Main program (named 'main') accepts a single command-line parameter that is the name of a data file containing actions to be performed on the symbol table. 

The following is a sample of the data file contents:
  ```
  beginscope
  define a 1
  use a
  endscope
  use a

  ```

Program scans through the data file in sequence and performs the necessary operations on the symbol table.

The output is identical to the input, except that each “use” line has the value of the constant indicated. 
For example, the above input file will result in the following output, printed to stdout:

```
  beginscope
  define a 1
  use a = 1
  endscope
  use a = undefined

```

Programming language used: Python 


### Hash-Table Plan and Structure
> Structure contains hashtable using an array with positions containing arraylists for variables and stack used for scoping.

[ al1 ] -> (:) -> (:)     [     ]
[     ]                   [ ar3 ] -> (:) -> (:)
[ al2 ]                   [     ]
[     ]                   [     ]
   ^                         ^
   |                         |
[  A _  _  _  _   _  _  _  _  _  _ B ]  -> Stack