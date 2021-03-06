from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import UploadJsonFile
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import System
from .formatters import SystemsFormatOne

__all__ = ['SystemsCreate']

# TODO - enforce use of create vs update by checking for existence of systemId


class SystemsCreate(UploadJsonFile, SystemsFormatOne):
    """Create a new System
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = SystemsFormatOne.get_parser(self, prog_name)
        parser = UploadJsonFile.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = SystemsFormatOne.before_take_action(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.handle_file_upload(parsed_args)

        headers = headers = SearchableCommand.headers(self, System,
                                                      parsed_args)
        rec = self.tapis_client.systems.add(body=self.json_file_contents)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
