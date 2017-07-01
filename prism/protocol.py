def get_protocol(app):
    if app.app_config['type'] == 'file':
        return File
    if app.app_config['type'] == 'git':
        return Git
    return None

def create(app, args):
    if args.file:
        return File.create(app, args)
    elif args.git:
        return Git.create(app, args)
    else:
        log.die('Create protocol failure.')

def build(app, args):
    return get_protocol(app).build(app, args)

class File:
    def create(app, args):
        app.app_config['type'] = 'file'
        app.app_config['locations'].append(args.file)
        return args.file

    def build(app, args):
        app.command.run('cp -R %s %s' % (app.app_config['source_folder'], app.app_env))

class Git:
    def create(app, args):
        log.die('Git not yet supported.')

    def build(app, args):
        log.die('Git not yet supported.')
