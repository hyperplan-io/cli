
from cmd import Cmd
from api import Api


from features_descriptors import create_features
from labels_descriptors import create_labels
from project import create_project
 


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
    def help_list(self):
        print('list requires an argument: features, labels, algorithms, projects')
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

    def help_create(self):
        print('create requires an argument: feature, label, algorithm, project')
    def complete_create(self, text, line, begidx, endidx):
        return [i
            for i in ('feature', 'label', 'algorithm', 'project')
            if i.startswith(text)]
    def do_create(self, inp):
        args = inp.split(' ')
        if len(args) > 0 and args[0] != '':
            arg = args[0]
            if arg == 'feature':
                create_features(self.api)
            elif arg == 'label':
                create_labels(self.api)
            elif arg == 'algorithm':
                self.api.create_algorithm()
            elif arg == 'project':
                create_project(self.api)
            else:
                print('Unknown argument {}'.format(arg))
        else:
            self.help_create()
    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')
    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
    do_EOF = do_exit
    help_EOF = help_exit
