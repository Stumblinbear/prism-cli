#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

import os

from .. import command
from .. import template


config_folder = '/etc/nginx/conf.d/'

def depends(app, args):
    command.Package.require('nginx')

def create(app, args):
    with open(os.path.join(config_folder, '%s.conf' % app.app_name), 'w') as file:
        format = {'app_env': app.app_env, 'listen': '', 'server_name': '', 'ssl': ''}
        for route in app.config['routes']:
            format['listen'] += 'listen %s;' % route['port']
            format['server_name'] += 'server_name %s;' % route['fqdn']
        file.write(template.get('exposer-nginx', format))

def destroy(app, args):
    if os.path.exists(os.path.join(config_folder, '%s.conf' % app.app_name)):
        command.run('rm -f %s' % os.path.join(config_folder, '%s.conf' % app.app_name))

def restart(app, args):
    if 'enabled' not in command.get_output_quiet('systemctl is-enabled nginx'):
        command.run('systemctl enable nginx')
    command.run('systemctl daemon-reload')
    command.run('systemctl restart nginx')
