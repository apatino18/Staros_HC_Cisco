"""starOS implementation of show_version.py

"""
import re
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any, Or, Schema

class ShowVersionSchema(MetaParser):
    """Schema for show version"""

    schema = {
        'version_info': {
            'version': str,
            'build': str,
            'description': str
        }     
    }


class ShowVersion(ShowVersionSchema):
    """Parser for show version"""

    cli_command = 'show version'

    """
    [local]staros-prueba# show version
    Active Software:
      Image Version:                  21.20.34
      Image Build Number:             85338
      Image Description:              Trusted_Deployment_Build
      Image Date:                     Sat May  7 06:54:18 EDT 2022
      Boot Image:                     /flash/staros.bin
      Source Commit ID:               6f2642692cdae18d56f9dbaa1dd39bcf245ad493
    """

    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        # initial return dictionary
        version_dict = {}
        
        result_dict = {}

        # initial regexp pattern
        p0 = re.compile(r'^(Image +Version\S\s+(?P<version_id>\d+\.\d+\.\d+))')
        p1 = re.compile(r'^(Image +Build +Number\S\s+(?P<build_id>\d+))')
        p2 = re.compile(r'^(Image +Description\S\s+(?P<description_id>\S+))')

        for line in out.splitlines():
            line = line.strip()

            m = p0.match(line)
            if m:
                if 'version_info' not in version_dict:
                    result_dict = version_dict.setdefault('version_info',{})
                version = m.groupdict()['version_id']
                result_dict['version'] = version
                
            m = p1.match(line)
            if m:
                if 'version_info' not in version_dict:
                    result_dict = version_dict.setdefault('version_info',{})
                build = m.groupdict()['build_id']
                result_dict['build'] = build

            m = p2.match(line)
            if m:
                if 'version_info' not in version_dict:
                    result_dict = version_dict.setdefault('version_info',{})
                description = m.groupdict()['description_id']
                result_dict['description'] = description
                continue

        return version_dict