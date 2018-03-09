import json

class base(object):
    _some_var = 'base class'
    def get_some(self):
        print(self._some_var)

class derived(base):
    _some_var = 'derived class'

class clothing_option(json.decoder):

    def __init__()

def main():
    b = base()
    d = derived()
    b.get_some()
    d.get_some()

if __name__ == '__main__':
    main()
