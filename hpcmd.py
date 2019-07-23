
from cmd import Cmd
from api import Api

class HyperplanPrompt(Cmd):
    prompt = 'hyperplan> '
    intro = "hyperplan-cli, Type ? to list commands"
    def __init__(self, api):
        Cmd.__init__(self)
        self.api = api
    def do_exit(self, inp):
        print("Bye")
        return True
    def do_login(self, inp):
        self.api.authenticate()
        print("Adding '{}'".format(inp))
    def help_list(self):
        print('list requires an argument: features, labels, algorithms, project')
    def complete_list(self, text, line, begidx, endidx):
        return [i
                for i in ('features', 'labels', 'algorithms', 'projects')
                if i.startswith(text)]
                    
    def do_list(self, inp):
        args = inp.split(' ')
        if len(args) > 0 and args[0] != '':
            arg = args[0]
            if arg == 'features':
                self.api.list_features()
            elif arg == 'labels':
                self.api.list_labels()
            elif arg == 'algorithms':
                self.api.list_algorithms()
            elif arg == 'projects':
                self.api.list_projects()
            else:
                print('Unknown argument {}'.format(arg))
        else:
            self.help_list()


    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')
    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
    do_EOF = do_exit
    help_EOF = help_exit
