import os
import json

import prism.log as log
from prism.config import save_config
from prism.config import config as prism_config
import prism.command

class App:
    def __init__(self, app_name):
        self.app_name = app_name
        self.command = AppCommand(self)

        self.app_src = None
        self.app_env = os.path.join('/etc/prism/env', self.app_name)
        self.app_folder = os.path.join(self.app_env, self.app_name)

        self.config = None

        if self.is_created:
            self.app_config = prism_config['apps'][self.app_name]

            self.app_src = self.app_config['source_folder']

            if type(self.app_config['config']) == str:
                load_from = self.app_config['config']
                if self.app_config['config'] == 'local':
                    load_from = os.path.join(self.app_config['source_folder'], 'prism.json')
                if not os.path.exists(load_from):
                    log.fail('Local config file does not exist. Generating...')
                    self.config = {}
                    self.save_config()
                else:
                    with open(load_from) as file:
                        try:
                            self.config = json.load(file)
                        except:
                            log.fail('Local config file load failed. Regenerating...')
                            self.config = {}
            else:
                self.config = self.app_config['config']

    @property
    def is_created(self):
        return self.app_name in prism_config['apps']

    def save_config(self):
        if not self.is_created:
            log.die('Attempt to save the config of an uncreated application.')

        if type(self.app_config['config']) == str:
            if self.app_config['config'] == 'local':
                if self.config is None:
                    log.fail('Application local config is borked. Regenerating...')
                    self.config = {}
                with open(os.path.join(self.app_config['source_folder'], 'prism.json'), 'w') as file:
                    json.dump(self.config, file)
            else:
                log.die('Unknown config setting.')
        else:
            save_config()

class AppCommand:
    def __init__(self, app):
        self.app = app

    def run(self, cmd, precmd=[], use_splitter=False):
        return prism.command.run(cmd, cwd=self.app.app_env, prefix='(app) ', precmd=precmd, use_splitter=use_splitter)

    def run_in_virtualenv(self, cmd, precmd=[], use_splitter=False):
        return prism.command.run(cmd, cwd=self.app.app_env, prefix='(app env) ', precmd=['source bin/activate']+precmd, use_splitter=use_splitter)
