#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

import os
import shutil

from ..deco import header, require_app, log_group
from .. import log
from .. import protocol
from .. import template

from .stop import run as action_stop
from .start import run as action_start
from .depends import run as action_depends
from .expose import run as action_expose


@header('App Updating')
@require_app
@log_group('Building application files...', 'Application tree generated')
def run(app, args):
    action_stop(app, args)

    if os.path.exists(app.app_folder):
        app.command.run('rm -rf %s' % app.app_folder)

    if os.path.exists(os.path.join(app.app_env, 'start.py')):
        app.command.run('rm -f %s' % os.path.join(app.app_folder, 'start.py'))
    elif os.path.exists(os.path.join(app.app_env, 'wsgi.py')):
        app.command.run('rm -f %s' % os.path.join(app.app_folder, 'wsgi.py'))

    # Rebuild the app environment
    protocol.build(app, args)

    # Install dependencies
    action_depends(app, args)

    # If there is a wsgi file, copy that to the environment base directory.
    start_file = ['wsgi.py', 'start.py']
    for f in start_file:
        if os.path.exists(os.path.join(app.app_folder, f)):
          log.info('Using %r in application files' % f)
          shutil.copyfile(os.path.join(app.app_folder, f), os.path.join(app.app_env, f))
          app.app_config['start_file'] = f
          break
    else:
        # If there is no start file, generate one.
        log.info('File not found. Generating \'start.py\'')
        with open(os.path.join(app.app_env, 'start.py'), 'w') as file:
            file.write(template.get('wsgi', {'app_name': os.path.basename(app.app_folder)}))

    # If there is no __init__.py, create one so it's recognized as a module
    if not os.path.exists(os.path.join(app.app_folder, '__init__.py')):
        log.info('Generating \'__init__.py\' in application files')
        open(os.path.join(app.app_folder, '__init__.py'), 'a').close()

    action_start(app, args)

    if app.is_exposed:
        action_expose(app, args)
