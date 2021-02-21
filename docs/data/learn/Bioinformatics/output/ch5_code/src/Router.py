if __name__ == '__main__':
    import importlib

    module_name = input()
    module = importlib.import_module(module_name)
    module.main()

