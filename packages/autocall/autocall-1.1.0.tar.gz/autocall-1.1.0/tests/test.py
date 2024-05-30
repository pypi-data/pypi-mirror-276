#!/bin/python3.10
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

@cmdline_default
def test6():
    print(f'test6()')
    
# main function
parse_and_run()
