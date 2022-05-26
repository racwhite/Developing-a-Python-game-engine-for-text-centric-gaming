"""
A quick example of how to put functions in a dictionary and then call them by their keys.
Also, how to pass an arbitrary amount of arguments to functions.
"""

def f_add(*args):
    """Adds numbers together, or just echoes a single number back."""
    value = None
    if len(args) == 0:
        return None
    else:
        value = int(args[0])
        for val in args[1:]:
            value += int(val)
    return value

def f_sub(*args):
    """
    Subtracts the second number from the first, or just negates a single number.
    Any other amount of arguments is considered incorrect.
    """
    value = None
    if len(args) < 1 or len(args) > 2:
        return None
    elif len(args) == 1:
        return -1 * int(args[0])
    else:
        value = int(args[0]) - int(args[1])
    return value

def f_print(*args):
    """Makes a string out of the given arguments, separating each by a space."""
    return '"' + " ".join(args) + '"'

# You can store and pass functions around by naming them (f_add) without calling them (f_add()).
function_dict = {"+": f_add,
                "-": f_sub,
                "p": f_print
                }

if __name__ == "__main__":
    # Sample commands that will get "parsed" and passed to the functions.
    lines = ["+ 2 2",  # adds up to 4
            "+ 42",  # echoes 42 back
            "+ 1 2 3 4 5",  # adds all up to 15
            "+",  # invalid, returns None
            "-",  # invalid, returns None
            "- 1",  # negates 1 to return -1
            "- -10",  # negates -10 to return 10
            "- 25 12",  # subtracts 12 from 25 to get 13
            "- 100 5 10 15 20",  # invalid, too many arguments, returns None
            "p Hi!",  # prints "Hi!"
            "p I've got a lovely bunch of coconuts",  # prints "I've got a lovely bunch of coconuts"
            "p there  they  are  all  standing  in  a  row",  # prints "there they are all standing in a row"
            "x This is a bad command!"  # unrecognized command, an error will print out
            ]
    
    # Looking at each line as a separate command.
    for line in lines:
        # Quick & dirty way to split a line into parts based on whitespace.
        components = line.split()
        
        # Convenience variables to keep easier track of which parts of each command are what.
        command = components[0]
        if len(components) > 1:
            arguments = components[1:]
        else:
            arguments = []
        
        # Check if a command is one we recognize. If so, invoke the appropriate command,
        # passing the rest of the arguments to it.
        # Print out whatever comes out of the functions.
        if command in function_dict.keys():
            print(function_dict[command](*arguments))
        else:
            print('ERROR: Unrecognized command "' + command + '"!')
