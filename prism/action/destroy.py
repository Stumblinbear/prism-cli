import os

from prism.deco import header, require_app, log_group
import prism.log as log
from prism.config import Static, save_config
from prism.config import config as prism_config
import prism.command as command


@header('App Destruction')
@require_app
@log_group('Destroying application...', 'Application destroyed.')
def run(app, args):
    del prism_config['apps'][app.app_name]
    save_config()

    command.run('rm -rf %s' % app.app_env)

    if os.path.exists(os.path.join(Static.nginx, '%s.conf' % app.app_name)):
        command.run('rm -f %s' % os.path.join(Static.nginx, '%s.conf' % app.app_name))

    if os.path.exists(os.path.join(Static.services, 'prism_%s.service' % app.app_name)):
        command.run('systemctl disable prism_%s' % app.app_name)
        command.run('systemctl stop prism_%s' % app.app_name)
        command.run('rm -f %s' % os.path.join(Static.services, 'prism_%s.service' % app.app_name))

        command.run('systemctl daemon-reload')
        command.run('systemctl restart nginx')
