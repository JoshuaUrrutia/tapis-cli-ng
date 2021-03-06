from agavepy.agave import AgaveError
from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import SystemRole
from .formatters import SystemsFormatMany

__all__ = ['SystemsRolesDrop']


class SystemsRolesDrop(SystemsFormatMany, ServiceIdentifier):
    """Drop all granted roles from a System
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(SystemsFormatMany, self).get_parser(prog_name)
        parser = ServiceIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = SystemsFormatMany.before_take_action(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.take_action_defaults(parsed_args)

        drop_result = self.tapis_client.systems.deleteRoles(
            systemId=parsed_args.identifier)
        if drop_result is not None:
            raise AgaveError('Failed to drop roles on {0}'.format(
                systemId=parsed_args.identifier))

        # Go ahead and list - should only return owner's role
        headers = SearchableCommand.headers(self, SystemRole, parsed_args)
        results = self.tapis_client.systems.listRoles(
            systemId=parsed_args.identifier)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
