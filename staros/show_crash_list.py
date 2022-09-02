"""starOS implementation of show_crash_list.py

"""
import re
from tokenize import Number
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any, Or, Schema

class ShowCrashListSchema(MetaParser):
    """Schema for show crash list"""

    schema = {
        'crash_table': {
            Any(): {
            'Date': str,
            'Instance': str,
            'CARD/CPU/PID': str,
            'SW Version': str,
            'MIO': str,
            },
        }    
    }
class ShowCrashList(ShowCrashListSchema):
    """Parser for show crash list"""

    cli_command = 'show crash list'

    """
=== ==================== ======== ========== =============== =======================
#           Time         Process  Card/CPU/        SW          HW_SER_NUM
                                     PID         VERSION       MIO / Crash Card
=== ==================== ======== ========== =============== =======================

1   2020-Oct-15+13:57:40 sessmgr  01/0/48672 21.13.1         FLM2236045H/FLM21500296
2   2020-Oct-15+14:06:56 sessmgr  01/0/48672 21.13.1         FLM2236045H/FLM21500296
3   2020-Oct-15+14:11:29 sessmgr  01/0/48672 21.13.1         FLM2236045H/FLM21500296
    """

    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        # initial return dictionary
        crash_dict = {}
        
        result_dict = {}

        # initial regexp pattern
        p0 = re.compile(r'^(?P<Number>\d+)\s+(?P<Date>\d+-\S+-\d+.\d+:\d+:\d+)\s+(?P<Instance>\S+)\s+(?P<Card_CPU_PID>\d+.\d+.\d+)\s+(?P<SW_Version>\d+.\d+.\d+)\s+(?P<card>\S+.\S+)')
        for line in out.splitlines():
            line = line.strip()

            m = p0.match(line)
            if m:
                if 'crash_table' not in crash_dict:
                    result_dict = crash_dict.setdefault('crash_table',{})
                Number = m.groupdict()['Number']
                Date = m.groupdict()['Date']
                Instance = m.groupdict()['Instance']
                Card_CPU_PID = m.groupdict()['Card_CPU_PID']
                SW_Version = m.groupdict()['SW_Version']
                card = m.groupdict()['card']

                result_dict[Number] = {}
                result_dict[Number]['Date'] = Date
                result_dict[Number]['Instance'] = Instance
                result_dict[Number]['CARD/CPU/PID'] = Card_CPU_PID
                result_dict[Number]['SW Version'] = SW_Version
                result_dict[Number]['MIO'] = card      
                continue

        return crash_dict