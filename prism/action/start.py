from ..deco import header, require_app, log_group

from .. import service


@header('Starting App')
@require_app
@log_group('Starting application service...', 'Service started')
def run(app, args):
    # Create the service files
    service.create(app, args)

    # Enable the service
    service.enable(app, args)

    # Start the service
    service.start(app, args)
