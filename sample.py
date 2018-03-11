import json

class base(object):
    _some_var = 'base class'
    def get_some(self):
        print(self._some_var)

class derived(base):
    _some_var = 'derived class'

messages = {
    'SKILL_NAME' : "What to wear outside",
    'HELP_MESSAGE': "Help",
    'STOP_MESSAGE': "Stop",
    'FINISHED_MESSSAGE':"Finished",
    'WELCOME_MESSAGE':"Welcome"
}

def message(msg_key):
    return messages[msg_key]

def main():
    print (message("SKILL_NAME"))
    print (message("HELP_MESSAGE"))

if __name__ == '__main__':
    main()
