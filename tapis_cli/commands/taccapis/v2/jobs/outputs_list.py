import os
from tapis_cli.display import Verbosity
from tapis_cli.commands.taccapis import SearchableCommand

from ..files.models import File
from ..files.formatters import FilesFormatMany, FilesOptions
from tapis_cli.clients.services.mixins import JobsUUID, RemoteFilePath
# Note - this is the jobs-outputs specific listdir!
from .helpers.walk import listdir

from . import API_NAME, SERVICE_VERSION


class JobsOutputsList(FilesFormatMany, JobsUUID, FilesOptions):
    """Lists a Jobs output directory
    """
    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = FilesFormatMany.get_parser(self, prog_name)
        parser = JobsUUID.extend_parser(self, parser)
        parser = RemoteFilePath.extend_parser(self, parser)
        parser = FilesOptions.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = FilesFormatMany.before_take_action(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.take_action_defaults(parsed_args)

        headers = SearchableCommand.headers(self, File, parsed_args)
        recs = listdir(parsed_args.file_path,
                       job_uuid=parsed_args.job_uuid,
                       agave=self.tapis_client)

        if not isinstance(recs, list):
            raise ValueError('No listing was returned')

        data = []

        # Fixes issue where the name of the listed file/directory is not
        # returned by the files service
        for rec in recs:
            row = []
            if rec['name'] == '.':
                rec['name'] = os.path.basename(rec['path'])

            for key in headers:
                try:
                    val = rec[key]
                except KeyError:
                    val = None
                row.append(val)
            data.append(row)

        # Sort must happen before humanize since it will affect sort order
        if parsed_args.ls_sort_time:
            sort_header = 'lastModified'
        elif parsed_args.ls_sort_size:
            sort_header = 'length'
        else:
            sort_header = 'name'
        data = self.sort_table(data,
                               headers,
                               header=sort_header,
                               reverse=parsed_args.ls_sort_reverse)

        return (tuple(headers), tuple(data))