# Simulator file for question 1.
# Fill in the implementation of the different commands of the simulator.
# You can use `tests.py` to run your simulator on some prewritten RAM programs.

from collections import defaultdict

variableList = []
# Note: defaultdict works exactly the same as a normal Python dictionary except it returns a default 
#       value (in this case, 0) when accessing a key that is not defined rather than raising KeyError.
#       We are using a dictionary rather than a list/array to manage the memory so that we don't need to 
#       initialize and store memory cells that are never accessed by the RAM program.
memory = defaultdict(int)

# Creates the variable list and the memory dictionary.
# Initializes the 0th variable, input_len, to be the first element of the program array.
def setupEnv(programArr, inputArr):
    # programArr as commands,
    # inputArr as inputs to program?

    variableList.clear()
    memory.clear()

    # for size of variable set in progArr[0], append 0s to variableList
    for i in range(programArr[0]):
        variableList.append(0)
    
    # set 0th variable of variable list to be the input_len
    variableList[0] = len(inputArr)

    # for the size of the input array, initialize the memory array with the input
    for i in range(len(inputArr)):
        memory[i] = inputArr[i]
        
# Runs the given RAM program on the input.
def executeProgram(programArr, inputArr):
    setupEnv(programArr, inputArr)
    
    # now programArr is just the commands
    programArr = programArr[1:]
    programCounter = 0

    while programCounter < len(programArr):
        # Store the command and the list of operands.
        cmd = programArr[programCounter][0]     # e.g. read, write, assign, arithmetic
        ops = programArr[programCounter][1:]    # e.g. operands of the command
        
        # Assignment commands
        if cmd == "read":
            # ['read', i, j]: lookup the var_j location in memory and assign that value to var_i                    
            variableList[ops[0]] = memory[variableList[ops[1]]]
        if cmd == "write":
            # ['write', i, j]: store the value of var_j in memory at the location var_i 
            memory[variableList[ops[0]]] = variableList[ops[1]]
        if cmd == "assign":
            # ['assign', i, j]: assign var_i to the value j @LIYA IS THIS RIGHT?
            variableList[ops[0]] = ops[1]
            
        # Arithmetic commands
        if cmd == "+":
            # ['+', i, j, k]: compute (var_j + var_k) and store in var_i
            variableList[ops[0]] = variableList[ops[1]] + variableList[ops[2]]
        if cmd == "-":
            # ['-', i, j, k]: compute max((var_j - var_k), 0) and store in var_i.
            variableList[ops[0]] = max((variableList[ops[1]] - variableList[ops[2]]),0)
            # variableList[ops[0]] = 0 if (variableList[ops[1]] - variableList[ops[2]] < 0) else variableList[ops[1]] - variableList[ops[2]]
        if cmd == "*":
            # ['*', i, j, k]: compute (var_j * var_k) and store in var_i.
            variableList[ops[0]] = variableList[ops[1]] * variableList[ops[2]]
        if cmd == "/":
            #  ['/', i, j, k]: compute (var_j // var_k) and store in var_i.
            variableList[ops[0]] = 0 if (variableList[ops[2]] == 0) else (variableList[ops[1]] // variableList[ops[2]])
            # Note that this is integer division. You should return an integer, not a float.
            # Remember division by 0 results in 0.
            
        # Control commands
        if cmd == "goto":
            # ['goto', i, j]: if var_i is equal to 0, go to line j
            if (variableList[ops[0]] == 0):
                programCounter = ops[1] - 1
        
        programCounter += 1
    
    # Return the memory starting at output_ptr with length of output_len
    return [memory[i] for i in range(variableList[1], variableList[1]+variableList[2])]