
from cmd import Cmd

from hyperplan.api import Api
from hyperplan.features_descriptors import create_features, describe_feature, list_features
from hyperplan.labels_descriptors import create_labels, describe_label, list_labels
from hyperplan.project import create_project, list_projects, update_project, describe_project
from hyperplan.algorithm import create_algorithm
from hyperplan.predict import predict

class HyperplanPrompt(Cmd):
    prompt = 'hyperplan> '
    intro = "hyperplan-cli, Type ? to list commands"
    def __init__(self, api):
        Cmd.__init__(self)
        self.api = api
        self.debug = False
    def do_exit(self, inp):
        print("Bye")
        raise Exception('')
    def do_login(self, inp):
        self.api.authenticate()
    def help_list(self):
        print('list requires an argument: features, labels, algorithms, projects')
    def complete_list(self, text, line, begidx, endidx):
        return [i
                for i in ('features', 'labels', 'algorithms', 'projects')
                if i.startswith(text)]
    def help_debug(self):
        print('debug requires true or false')
    def do_debug(self, inp):
        args = inp.split(' ')
        if len(args) > 0 and args[0] != '':
            arg = args[0]
            if arg.lower() == 'true':
                self.debug = True
            elif arg.lower() == 'false':
                self.debug = False 
            else:
                print('{} is not a boolean'.format(arg))
        else:
            self.help_debug()

    def do_list(self, inp):
        args = inp.split(' ')
        if len(args) > 0 and args[0] != '':
            arg = args[0]
            if arg == 'features':
                list_features(self.api)
            elif arg == 'labels':
                list_labels(self.api)
            elif arg == 'algorithms':
                pass
            elif arg == 'projects':
                list_projects(self.api)
            else:
                print('Unknown argument {}'.format(arg))
        else:
            self.help_list()

    def help_describe(self):
        print('describe requires the entity type (feature, label, algorithm, project) and the entity id')
    def help_create(self, example=None):
        if example == None:
            print('create requires an argument: feature, label, algorithm, project and the id')
            print('example: create feature myFeature')
        else:
            print('create requires an argument: feature, label, algorithm, project and the id')
            print('example: create {} my{}'.format(example, example.capitalize()))
    def help_update(self):
        print('update requires an argument: project and the id')
        print('example: update project myProject')

    def complete_describe(self, text, line, begidx, endidx):
        return [i
            for i in ('feature', 'label', 'algorithm', 'project')
            if i.startswith(text)]
    def complete_create(self, text, line, begidx, endidx):
        return [i
            for i in ('feature', 'label', 'algorithm', 'project')
            if i.startswith(text)]
    def complete_update(self, text, line, begidx, endidx):
        return [i
            for i in (['project'])
            if i.startswith(text)]
    def do_create(self, inp):
        args = inp.split(' ')
        if len(args) > 1 and args[0] != '' and args[1] != '':
            arg = args[0]
            entity_id = args[1]
            if arg == 'feature':
                create_features(self.api, entity_id)
            elif arg == 'label':
                create_labels(self.api, entity_id)
            elif arg == 'algorithm':
                create_algorithm(self.api, entity_id)
            elif arg == 'project':
                create_project(self.api, entity_id)
            else:
                print('Unknown argument {}'.format(arg))
        elif len(args) == 1 and args[0] != '':
            self.help_create(example=args[0])
        else:
            self.help_create(example=None)
    def do_update(self, inp):
        args = inp.split(' ')
        if len(args) > 1 and args[0] != '' and args[1] != '':
            arg = args[0]
            entity_id = args[1]
            update_project(self.api, entity_id)
        else:
            self.help_update()


    def do_describe(self, inp):
        args = inp.split(' ')
        if len(args) > 1 and args[0] != ''and args[1] != '':
            arg = args[0]
            entity_id = args[1]
            if arg == 'feature':
               describe_feature(self.api, entity_id)
            elif arg == 'label':
               describe_label(self.api, entity_id)
            elif arg == 'algorithm':
                pass
            elif arg == 'project':
                describe_project(self.api, entity_id)
            else:
                print('Unknown argument {}'.format(arg))
        else:
            self.help_describe()
    def help_predict(self):
        print('predict requires a project id as argument')
    def do_predict(self, inp):
        args = inp.split(' ')
        if len(args) > 0 and args[0] != '':
            project_id = args[0]
            prediction = predict(self.api, project_id, log=True)
        else:
            self.help_predict()

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')
    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
    do_EOF = do_exit
    help_EOF = help_exit
