#!/bin/python3
import inspect
import sys

# functions taged by @cmdline
__register_funcs = []
__register_funcs_default = []

def colorize(text, color):
    return f"\033[{color}m{text}\033[0m"

def cmdline_default(func):
    funcname = func.__name__
    parameters = inspect.getfullargspec(func)

    if len(parameters.args) != 0 and len(parameters.args) != len(parameters.defaults):
            print(colorize(f'[Autocall Warning]: arguments of function \'{funcname}\' should be optional.', 34))
            return func
    
    __register_funcs_default.append(func)

    if func not in __register_funcs:
        __register_funcs.append(func)
    
    globals()[funcname] = func
    return func

def cmdline(func):
    if func in __register_funcs:
        return func
    
    __register_funcs.append(func)
    globals()[func.__name__] = func
    return func

def parse_run(argv = sys.argv[1:]):
    __argv = []

    def str_to_any(_str, _type):
        if _type == int:
            return int(_str, 0)
        elif _type == str:
            return _str
        else:
            raise Exception("Don't know the type")

    def match_and_check(name):
        res = [f for f in __register_funcs if f.__name__ == name]
        res += [f for f in __register_funcs_default if f.__name__ == name]
        if not res:
            raise Exception("Couldn't found function")

        #if len(getfullargspec(res[0]).args) != len(res[0].__annotations__):
            #raise Exception("Target function's arguments should have determinded types")

        return res[0]

    # register this function into __register_funcs list
    @cmdline
    def help(verbose :str = 'notverbose'):
        'Give the argument \"verbose\" instead of \"notverbose\" to print detail information.'
        print('Help Tips Provided by Autocall.')
        print('  option:')

        for func in __register_funcs:
            parameters = inspect.signature(func).parameters
            print(f'    --{func.__name__:<10s}', end='')
            for name in parameters:
                anno = parameters[name].annotation
                defa = parameters[name].default

                if anno != inspect._empty:
                    if type(anno) != type:
                        anno = f'({anno})'
                    else:
                        anno = f'({anno.__name__})'
                else:
                    anno = ''

                if verbose == 'notverbose':
                    anno = ''
                    
                if defa != inspect._empty:
                    defa = f'[{name}{anno} = {defa}]'
                else:
                    defa = f'{name}{anno}'
                
                print(f'{defa}  ', end='')
                
            print()
            if func.__doc__:
                print(f'                {func.__doc__:>20s}')
            if func in __register_funcs_default:
                print(f'                The function will be called directly if not specific.')
            print()

    
    # Parsing
    for arg in argv:
        if arg.startswith('--'):
            __argv.append([arg[2:]])
        elif arg.startswith('-'):
            __argv.append([arg[2:]])
        else:
            if not len(__argv):
                continue
            # -1 indicate one existed function name. arg will be appended after the function name into a new string.
            __argv[-1].append(arg)

    # Call function
    if not len(__argv):
        __argv = [[funcname.__name__] for funcname in __register_funcs_default]
    #print(__argv)
    
    for item in __argv:
        name = item[0]
        func = match_and_check(name)
        args = inspect.getfullargspec(func).args
        anns = func.__annotations__

        arguments = ', '.join([(lambda argname, passvalue:
                          passvalue if anns.get(argname) != str
                          else f'\'{passvalue}\'')(k, v)
                         for k, v in zip(args, item[1:])])

        #print(globals())
        eval(f'{name}({arguments})')
