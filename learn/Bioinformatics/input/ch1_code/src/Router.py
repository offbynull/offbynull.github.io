if __name__ == '__main__':
    module_name = input()
    module = __import__(module_name)
    module.main()

