import os

from prism.deco import header, require_app
import prism.log as log
import prism.command as command
from prism.config import Static
import prism.template


@header('App Nginx Exposer')
@require_app
def run(app, args):
    if 'routes' not in app.config:
        log.fail('No routes set. Nothing to change.')
        return

    if 'exposed' not in app.config:
        app.config['exposed'] = False
        app.save_config()

    if args.action == 'expose':
        app.config['exposed'] = not app.config['exposed']
        app.save_config()

    elif 'exposed' not in app.config or not app.config['exposed']:
        log.fail('Application not exposed. To expose your app through Nginx, run: prism -a app_name expose')
        return

    if app.config['exposed']:
        log.doing('Exposing application via Nginx...')

        with open(os.path.join(Static.nginx, '%s.conf' % app.app_name), 'w') as file:
            format = {'listen': '', 'server_name': '', 'ssl': ''}
            for route in app.config['routes']:
                format['listen'] += 'listen %s;' % route['port']
                format['server_name'] += 'server_name %s;' % route['fqdn']
            format['app_env'] = app.app_env
            file.write(prism.template.get('nginx', format))

        with open(os.path.join(Static.services, 'prism_%s.service' % app.app_name), 'w') as file:
            file.write(prism.template.get('service', {'app_name': app.app_name, 'app_env': app.app_env, 'environment': '', 'workers': 3}))

        command.run('systemctl daemon-reload')
        command.run('systemctl enable prism_%s' % app.app_name)
        command.run('systemctl start prism_%s' % app.app_name)
        command.run('systemctl restart nginx')

        log.action('Nginx config generated, application exposed successfully.')
    else:
        log.doing('Unexposing application via Nginx...')

        command.run('systemctl disable prism_%s' % app.app_name)
        command.run('systemctl stop prism_%s' % app.app_name)
        command.run('systemctl restart nginx')

        log.fail('Application no longer exposed. Run the command again to re-expose the application.')
