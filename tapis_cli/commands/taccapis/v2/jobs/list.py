from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import Job
from .formatters import JobsFormatMany

__all__ = ['JobsList']


class JobsList(JobsFormatMany):
    """List Job records and status
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.LISTING

    def get_parser(self, prog_name):
        parser = super(JobsFormatMany, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        parsed_args = JobsFormatMany.before_take_action(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.take_action_defaults(parsed_args)

        headers = SearchableCommand.headers(self, Job, parsed_args)
        results = self.requests_client.get_data(params=self.post_payload)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))
