import os


def get(name, formatting={}):
    with open(os.path.join(os.path.dirname(__file__), 'templates', name + '.pl8')) as file:
        return ''.join(file.readlines()).format(**formatting)
