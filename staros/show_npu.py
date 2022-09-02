"""starOS implementation of show_npu_utilization_table.py

"""
import re
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any, Or, Schema

class ShowNpuSchema(MetaParser):
    """Schema for show npu utilization table"""

    schema = {
        'npu_utilization_table': {
            Any(): {
                'NPU NOW': str,
                'NPU MIN5': str,
                'NPU MIN15': str
            },
        }    
    }


class ShowNpu(ShowNpuSchema):
    """Parser for show npu utilization table"""

    cli_command = 'show npu utilization table'

    """
 ---------npu--------
     npu     now   5min  15min
--------  ------ ------ ------
 05/0/01      0%     0%     0%
 05/0/02      0%     0%     0%
 05/0/03      0%     0%     0%
 05/0/04      0%     0%     0%
 06/0/01      0%     0%     0%
 06/0/02      0%     0%     0%
 06/0/03      0%     0%     0%
 06/0/04      0%     0%     0%             
    
    """

    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        # initial return dictionary
        recovery_dict = {}
        
        result_dict = {}

        # initial regexp pattern
        p0 = re.compile(r'(?P<npu>\d+.\d+.\d+.)\s+(?P<npu_now>\d+.)\s+(?P<npu_min5>\d+.)\s+(?P<npu_min15>\d+.)')
        for line in out.splitlines():
            line = line.strip()

            m = p0.match(line)
            if m:
                if 'npu_utilization_table' not in recovery_dict:
                    result_dict = recovery_dict.setdefault('npu_utilization_table',{})
                npu = m.groupdict()['npu']
                npu_now = m.groupdict()['npu_now']
                npu_min5 = m.groupdict()['npu_min5']
                npu_min15 = m.groupdict()['npu_min15']
                result_dict[npu] = {}
                result_dict[npu]['NPU NOW'] = npu_now
                result_dict[npu]['NPU MIN5'] = npu_min5
                result_dict[npu]['NPU MIN15'] = npu_min15        
                continue
        return recovery_dict