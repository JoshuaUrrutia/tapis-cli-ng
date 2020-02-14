from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from .mixins import ActorIdentifier

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne

__all__ = ['ActorsAliasesCreate']


class ActorsAliasesCreate(ActorsFormatOne, ActorIdentifier):
    """Add an alias of an actor
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(ActorsAliasesCreate, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        parser.add_argument('alias',
                            metavar='<ALIAS>',
                            type=str,
                            help='The alias to create')
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)
        alias = parsed_args.alias
        body = {
            'actorId': actor_id,
            'alias': alias
        }
        rec = self.tapis_client.actors.addAlias(body=body)
        headers = ["actorId", "alias", "owner"]
        data = []
        for key in headers:
            try:
                val = rec[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))