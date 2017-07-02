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


config_folder = '/etc/httpd/conf.d/'

def depends(app, args):
    command.Package.require('httpd')

def create(app, args):
    # SSL: SSLRequireSSL
    # RequestHeader set X-FORWARDED-PROTOCOL ssl
    # RequestHeader set X-FORWARDED-SSL on
    with open(os.path.join(config_folder, '%s.conf' % app.app_name), 'w') as file:
        format = {'app_env': app.app_env, 'app_name': app.app_name, 'named_host': '', 'listen': '', 'ports': '', 'server_name': '', 'ssl': ''}
        for route in app.config['routes']:
            format['named_host'] += 'NameVirtualHost *:%s' % route['port']
            if route['port'] != 80 and route['port'] != 443:
                format['listen'] += 'Listen %s\n' % route['port']
            format['ports'] += ' *:%s' % route['port']

            if len(format['server_name']) == 0:
                format['server_name'] += 'ServerName %s' % route['fqdn']
            elif 'ServerAlias' not in format['server_name']:
                format['server_name'] += '\nServerAlias %s' % route['fqdn']
            else:
                format['server_name'] += ' %s' % route['fqdn']
        file.write(template.get('exposer-apache', format))

def destroy(app, args):
    if os.path.exists(os.path.join(config_folder, '%s.conf' % app.app_name)):
        command.run('rm -f %s' % os.path.join(config_folder, '%s.conf' % app.app_name))

def restart(app, args):
    if 'enabled' not in command.get_output_quiet('systemctl is-enabled httpd'):
        command.run('systemctl enable httpd')
    command.run('systemctl daemon-reload')
    command.run('systemctl restart httpd')
