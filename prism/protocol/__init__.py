import inspect

from .. import log


def get_protocol(app):
    try:
        mod = __import__('prism.protocol.%s' % app.app_config['type'], globals(), locals(), ['object'], 0)
        return mod
    except:
        log.die('Protocol %r failure.' % app.app_config['type'])

def create(app, args):
    return get_protocol(app).create(app, args)

def build(app, args):
    return get_protocol(app).build(app, args)
