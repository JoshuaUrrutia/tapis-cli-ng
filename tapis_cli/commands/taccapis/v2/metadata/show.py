from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import ServiceIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import Metadata
from .formatters import MetadataFormatOne
from .mixins import MetadataIdentifier

__all__ = ['MetadataShow']


class MetadataShow(MetadataFormatOne, MetadataIdentifier):
    """Show a Metadata document by UUID
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(MetadataShow, self).get_parser(prog_name)
        parser = MetadataIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION, 'data')
        self.update_payload(parsed_args)

        headers = self.render_headers(Metadata, parsed_args)
        identifier = parsed_args.identifier
        self.validate_identifier(identifier)
        rec = self.tapis_client.meta.getMetadata(uuid=parsed_args.identifier)

        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))
