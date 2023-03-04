if __name__ == '__main__':
    import importlib

    val = input()
    val = val.split()
    if len(val) == 1:
        module_name = val[0]
        function_name = 'main'
    elif len(val) == 2:
        module_name = val[0]
        function_name = val[1]
    else:
        raise ValueError(f'Too many parameters: {val}')
    module = importlib.import_module(module_name)
    getattr(module, function_name)()
