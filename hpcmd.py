
from cmd import Cmd
from api import Api
from prettytable import PrettyTable

def qcm(choice_1, choice_2, choice_3):
    print('1. Create a new feature')
    print('2. Stop and create')
    print('3. Stop and erase')
    choice = input('Choose: ')
    if choice == '1':
        return choice_1()
    elif choice == '2':
        return choice_2()
    elif choice == '3':
        return choice_3()
    else:
        return qcm(choice_1, choice_2, choice_3)

def create_single_feature():
    print("============== Create feature")
    name = input('name: ')
    feature_type = input('type(string, float, int): ')
    dimension = input('dimension(one, array, matrix): ')
    description = input('description: ')
    print("==============")
    return [name, feature_type, dimension, description]
def post_features():
    return []
def noop():
    return []

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
                table = PrettyTable(['Name', 'Type', 'Dimension', 'Description'])
                feature_name = input('id: ')
                features = [[]]
                while True:
                    table.add_row(qcm(create_single_feature, post_features, noop))
                    print(table)
                self.api.create_feature()
            elif arg == 'label':
                self.api.create_label()
            elif arg == 'algorithm':
                self.api.create_algorithm()
            elif arg == 'project':
                self.api.create_project()
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
