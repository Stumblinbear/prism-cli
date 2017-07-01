from prism.deco import require_app, log_group
import prism.log as log


@require_app
@log_group('Application restarting...', 'Restarted.')
def run(app, args):
    pass
