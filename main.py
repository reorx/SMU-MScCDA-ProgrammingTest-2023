from importlib import import_module


if __name__ == '__main__':
    n = input('Please enter the question number (1/2/3): ')
    module_name = f'question_{n}'
    import_module(module_name).main()
