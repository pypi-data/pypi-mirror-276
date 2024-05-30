# Call function directly in cmd line

#### Features
1. Allow user call functions directly in command line.
2. Generate help tips automatically.
3. Add default called functions if not function was specific.

#### Notice
1. It's better to add argument type for each autocall functions.
2. str type argument must be defined explicitly.
3. @cmdline_default is a subset of @cmdline, which means function with @cmdline_default will have @cmdline implicitly.
4. Arguments of function with @cmdline_default should be optional or no argument.

#### TODO
1. Support class's function with self as the first argument.

#### Code example
``` python
#!/bin/python3.8
from autocall import *

# The tar @cmdline is used to register the function.
@cmdline
def test1():
    print(f'test1()')
    pass

@cmdline
@cmdline_default
def test2(arg: int = 0):
    print(f'test2({arg})')
    pass

@cmdline
def test3(arg1, arg2: str = 'this is a string'):
    print(f'test3({arg1}, {arg2})')
    
@cmdline
def test4(arg1, arg2: int):
    'You can add some extra information here.'
    print(f'test4({arg1}, {arg2})')
    pass

@cmdline_default
def test5(arg1: int = 1, arg2: str = 'good'):
    print(f'test5({arg1}, {arg2})')

# main function
parse_and_run()
```
#### Run the code
``` bash
~/autocall/src $ ./test.py --help
Help Tips Provided by Autocall.
  option:
    --test1     

    --test2     [arg = 0]  
                The function will be called directly if not specific.

    --test3     arg1  [arg2 = this is a string]  

    --test4     arg1  arg2  
                You can add some extra information here.

    --test5     [arg1 = 1]  [arg2 = good]  
                The function will be called directly if not specific.

    --help      [verbose = notverbose]  
                Give the argument "verbose" instead of "notverbose" to print detail information.

~/autocall/src $ ./test.py --test5 10 'hello'
test5(10, hello)
~/autocall/src $ ./test.py
test2(0)
test5(1, good)
```
