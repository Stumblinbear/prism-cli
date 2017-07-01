import os

from prism.deco import header, require_app, log_group
import prism.log as log
from prism.config import Static, save_config
from prism.config import config as prism_config
import prism.command as command
import prism.protocol as protocol
from prism import App

import prism.action.update

@header('App Creation')
@require_app(inverse=True)
@log_group('Creating application...', 'Application created.')
def run(app, args):
    command.run('virtualenv %s' % app.app_name, use_splitter=True)

    prism_config['apps'][app.app_name] = Static.default_app_config
    app.app_config = prism_config['apps'][app.app_name]

    app.app_config['locations'].append(app.app_env)

    app.app_config['source_folder'] = protocol.create(app, args)

    if args.local_config or os.path.exists(os.path.join(app.app_config['source_folder'], 'prism.json')):
        app.app_config['config'] = 'local'

    save_config()

    app = App(app.app_name)
    prism.action.update.run(app, args)
    app.save_config()
