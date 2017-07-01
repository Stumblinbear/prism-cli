from ..deco import header, require_app, log_group
from .. import log

from .start import run as action_start
from .stop import run as action_stop


@header('Restarting App')
@require_app
@log_group('Application service restarting...', 'Restarted')
def run(app, args):
    action_stop(app, args)
    action_start(app, args)
