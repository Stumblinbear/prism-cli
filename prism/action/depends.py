import os

from prism.deco import header, require_app, log_group
import prism.log as log


@header('App Depends Install')
@require_app
@log_group('Installing requirements...', 'Requirements installed.')
def run(app, args):
    app.command.run_in_virtualenv('pip install gunicorn', use_splitter=True)

    if os.path.exists(os.path.join(app.app_folder, 'requirements.txt')):
        app.command.run_in_virtualenv('pip install -r requirements.txt', precmd=['cd ' + app.app_name], use_splitter=True)
    else:
        log.info('No requirements.txt, skipping dependency install.')
