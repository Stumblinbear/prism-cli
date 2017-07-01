import os
import shutil

from prism.deco import header, require_app, log_group
import prism.log as log
import prism.protocol as protocol
import prism.template

import prism.action.depends


@header('App Updating')
@require_app
@log_group('Building application files...', 'Application tree generated.')
def run(app, args):
    if os.path.exists(app.app_folder):
        app.command.run('rm -rf %s' % app.app_folder)

    if os.path.exists(os.path.join(app.app_env, 'wsgi.py')):
        app.command.run('rm -rf %s' % os.path.join(app.app_folder, 'wsgi.py'))

    protocol.build(app, args)

    prism.action.depends.run(app, args)

    if os.path.exists(os.path.join(app.app_folder, 'wsgi.py')):
        log.info('Using \'wsgi.py\' in application files')
        shutil.copyfile(os.path.join(app.app_folder, 'wsgi.py'), os.path.join(app.app_env, 'wsgi.py'))
    else:
        log.info('File not found. Generating wsgi.py')
        with open(os.path.join(app.app_env, 'wsgi.py'), 'w') as file:
            file.write(prism.template.get('wsgi', {'app_name': os.path.basename(app.app_folder)}))

    if not os.path.exists(os.path.join(app.app_folder, '__init__.py')):
        log.info('Generating \'__init__.py\' in application files')
        open(os.path.join(app.app_folder, '__init__.py'), 'a').close()
