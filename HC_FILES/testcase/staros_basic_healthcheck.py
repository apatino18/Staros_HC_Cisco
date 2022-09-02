from os import device_encoding
from pyats import aetest
from genie import testbed
import logging
from datetime import datetime
from statistics import median,stdev,mean

log = logging.getLogger(__name__)
class Device_Connection(aetest.CommonSetup):
    @aetest.subsection
    def connect_to_device(self, device):
        log.info("Aetest Common Setup ")
        # connect to testbed devices
        device.connect()
        

class GENERAL(aetest.Testcase):
    @aetest.test        
    def show_card_table(self, device):
        # configure each device interface
        show_card_table = device.parse('show card table')
        for values in show_card_table['card_table']:
            SPOF=show_card_table['card_table'][values]['SPOF']
            if 'YES' in SPOF:
                self.failed("Card num : {} marked as SPOF".format(show_card_table['card_table'][values]))
    @aetest.test        
    def show_temperature(self, device):
        # configure each device interface
        show_temp = device.parse('show temperature')
        for key,values in show_temp['temperature_table'].items():
            STATE=values['STATE']
            if 'Normal' not in STATE:
                self.failed("Card {} is on {} state".format(key,values['STATE']))
    @aetest.test    
    def show_fans(self, device):
        # configure each device interface
        show_fan = device.parse('show fans')
        for key in show_fan['fan_info']:
            if 'Normal' == show_fan['fan_info'][key]['State']:
                log.info('Fan in {}is in State {} Temperature {} '.format(key,show_fan['fan_info'][key]['State'],show_fan['fan_info'][key]['Temperature']))
                continue
            else:
                self.failed('Fan in {}is in State {} Temperature {} '.format(key,show_fan['fan_info'][key]['State'],show_fan['fan_info'][key]['Temperature']))
    @aetest.test    
    def show_hd_raid_verbose(self, device):
        # configure each device interface
        show_raid = device.parse('show hd raid verbose')
        if show_raid['raid_table']['DEGRADED'] != 'No':
            self.failed('The HD-RAID is degraded')
    @aetest.test    
    def show_power(self, device):
        # configure each device interface
        show_power = device.parse('show power chassis')
        if 'All power sources are good' not in show_power['power_info']['Message']:
            self.failed('Error: {}'.format(show_power['power_info']['Message']))
            

class SYSTEM(aetest.Testcase): 
    @aetest.test
    def show_version(self, device):
        # configure each device interface
        log.info("Second test section ")
        self.show_version_output = device.parse('show version')
        if 'Deployment_Build' in self.show_version_output['version_info']['description']:
            log.info("System Version :{} OK!! ".format(self.show_version_output['version_info']['version']))
        else:
            self.failed("Current Version :{} is not deployment".format(self.show_version_output['version_info']['version']))               
    @aetest.test        
    def show_card_hardware(self, device):
        # configure each device interface
        show_card = device.parse('show card hardware')
        for key, value in show_card['hardware_table'].items():
            if ' up to date' == show_card['hardware_table'][key]['Card Programmables']:
                log.info('{} type {} is up to date'.format(key,show_card['hardware_table'][key]['Card Type']))
            else:
                self.failed('Error {} type{} is {}'.format(key,show_card['hardware_table'][key]['Card Type'],show_card['hardware_table'][key]['Card Programmables']))
    @aetest.test    
    def show_cpu_table(self, device,HC_param):
        # configure each device interface
        show_cpu = device.parse('show cpu table')
        for key in show_cpu['cpu_table'].keys():
            if 'M' in show_cpu['cpu_table'][key]['mem 5min']:
                mem_megas = float(show_cpu['cpu_table'][key]['mem 5min'].strip("M"))
                mem5min = mem_megas/1000
                continue
            mem5min = float(show_cpu['cpu_table'][key]['mem 5min'].strip("G"))
            memtotal = float(show_cpu['cpu_table'][key]['mem total'].strip("G"))
            mempercent= (mem5min*100)/memtotal
            cpu5min = float(show_cpu['cpu_table'][key]['cpu 5min'].strip("%"))
            if mempercent > HC_param.memory_usage or cpu5min > HC_param.cpu_usage:
                self.failed('AvG Mem is over 50%, current values Mem:{}% and CPU:{}%'.format(mempercent,cpu5min))
            else:
                log.info('CPU {} Memory {}%  CPU {}%'.format(key,int(mempercent),cpu5min))      
    @aetest.test        
    def show_bulkstats(self, device,HC_param):
        # configure each device interface
        show_bulkstats = device.parse('show bulkstats')
        for key, value in show_bulkstats['bulkstats_info'].items():
            if int(key) > 1:
                transmitted = int(show_bulkstats['bulkstats_info'][key]['Records Transmitted'])
                collected = int(show_bulkstats['bulkstats_info'][key]['Records Collected'])
                success_rate= ((transmitted*100)/collected)
                if success_rate > HC_param.bulk_success_rate:
                    log.info('Bulkstats Collected agains transmitted ratio is : {}%'.format(success_rate))
                else:
                    self.failed('Issue with ratio of collected bulkstats against transmitted')
            if int(key) > 1:
                if show_bulkstats['bulkstats_info'][key]['Last Succesful transfer'] == show_bulkstats['bulkstats_info'][key]['Last Attemped transfer']:
                    log.info("Bulkstats file {} are sent to destination succesfully".format(key))
                else:
                    self.failed('Last attempt to sent bulkstats from file {} failed'.format((key)))
    @aetest.test    
    def show_license_info(self, device,HC_param):
        # configure each device interface
        show_license = device.parse('show license information')
        if 'Expires' not in show_license['license_info']['information'].keys():
            pass
        else:
            exp_date = show_license['license_info']['information']['Expires']['Year']+ "-"+show_license['license_info']['information']['Expires']['Month']+ "-"+show_license['license_info']['information']['Expires']['Day']
            date_translated =datetime.strptime(exp_date, "%Y-%B-%d")
            date_now=datetime.now()
            time_to_exp=date_translated - date_now
            if time_to_exp.days < HC_param.license_exp_days:
                self.failed('Error License is about to expire in : {} days'.format(time_to_exp.days))
            else:
                log.info("Time to license expiration: {} days ".format(time_to_exp.days))

        if 'Matches' != show_license['license_info']['information']['Status']['Chassis MEC'] or 'Good' != show_license['license_info']['information']['Status']['Status']:
            self.failed('Error License MEC {} status {}'.format(show_license['license_info']['information']['Status']['Chassis MEC'], show_license['license_info']['information']['Status']['Status']))
    @aetest.test    
    def show_resources(self, device):
        # configure each device interface
        show_resources = device.parse('show resources')
        for key,value in show_resources['resources_info'].items():
            if 'Acceptable Limits' not in value['License']:
                self.failed('Error License for {} is {}'.format(key,value['License']))
    @aetest.test    
    def show_session_recovery(self, device):
        # configure each device interface
        show_recovery = device.parse('show session recovery status verbose')
        for key,value in show_recovery['session_recovery_table'].items():
            if 'Good' not in value['STATUS']:
                self.failed('Error CPU {} is in status {}'.format(key,value['STATUS']))
    @aetest.test    
    def show_system_uptime(self, device,HC_param):
        # configure each device interface
        show_uptime = device.parse('show system uptime')
        days = int(show_uptime['uptime_info']['DAYS'].strip('D'))
        if days < HC_param.days_up:
            self.failed('Last reload of the node hours: {}'.format(show_uptime['uptime_info']['HOURS']))


class ALARMS(aetest.Testcase):    
    @aetest.test        
    def show_alarm_all(self, device,HC_param):
        # configure each device interface
        show_temp = device.parse('show alarm all')
        for key, value in show_temp['alarms']['Statistics']['Current'].items():
            if int(value) >= HC_param.critical_alarm and 'TOTAL' not in key :
                self.failed('{} alarm :{}'.format(key,value))
    @aetest.test    
    def show_crash_list(self, device,HC_param):
        # configure each device interface
        show_crash = device.parse('show crash list')
        latest_bug=list(show_crash['crash_table'])[-1]
        date_lastest_bug=show_crash['crash_table'][latest_bug]['Date']
        date_now=datetime.now()
        date_bug_translated =datetime.strptime(date_lastest_bug, "%Y-%b-%d+%H:%M:%S")
        time_since_last_bug=date_now-date_bug_translated
        if time_since_last_bug.days > HC_param.bug_days:
            log.info('Last Bug Present  for Instance:{} on Date {}'.format(show_crash['crash_table'][latest_bug]['Instance'],date_bug_translated))
        else:
            self.failed('Last Bug Present  for Instance:{} on Date {} please review the crash'.format(show_crash['crash_table'][latest_bug]['Instance'],date_bug_translated))    
    @aetest.test    
    def show_task_sessmgr(self, device):
        # configure each device interface
        show_task = device.parse('show task resources facility sessmgr all')
        for key, values in show_task['task_table'].items() :
            if 'good' not in values['Status']:
                self.failed('Sessmgr for CPU {} instance {} is in state: {}'.format(values['CPU'],key,values['Status'])) 
    @aetest.test    
    def show_snmp_trap(self, device,HC_param):
        # configure each device interface
        snmp_trap = device.parse('show snmp trap history')
        trap_list_critical= ["CardRemoved","PortLinkDown","CardDown","BGPPeerSessionDown","DiameterPeerDown","PortDown","BGPPeerSessionIPv6Down","SERDESLanePermanentlyDown","DDFreload","CiscoFruRemoved","CiePortLinkDown"]
        trap_list= ["CardRemoved","PortLinkDown","AAAAccSvrReachable","CardDown","ManagerFailure","CGFDead","NTPPeerUnreachable","BGPPeerSessionDown","CardSPOFAlarm","TaskFailed","DiameterPeerDown","PortDown","CPUOver","BFDSessionDown","BGPPeerSessionIPv6Down","SERDESLanePermanentlyDown","DDFreload","CiscoFruRemoved","CiePortLinkDown"]
        trap_count = 0
        trap_failure=[]
        for trap, data in snmp_trap['snmp_info'].items():
            if data['Trap'] in trap_list_critical:
                log.info('Trap {} generated on {} at {} review log!!'.format(data['Trap'],data['Date'],data['Time']))
                trap_failure.append(data['Trap'])
                trap_count +=3
            elif data['Trap'] in trap_list:
                log.info('Trap {} generated on {} at {} review log!!'.format(data['Trap'],data['Date'],data['Time']))
                trap_count +=1
                trap_failure.append(data['Trap'])
        if trap_count >= HC_param.trap_failure:
            self.failed('Error the follow traps appeared on history : {}'.format(list(set(trap_failure))))  


class PORTS(aetest.Testcase): 
    @aetest.test    
    def show_port_table(self, device):
        # configure each device interface
        show_port = device.parse('show port table')
        lac_main_ports= ['5/10','5/11','6/10','6/11']
        for key, value in show_port['port_table'].items():
            if  value['Redundant'] == 'L2' or value['Redundant'] == 'LA+':
                pass
            else:
                self.failed('Port {} Operation: {} Link: {} Pair {} Redundant {} out of LAC'.format(key,value['Operation'],value['Link'],value['Pair'],value['Redundant']))
            if 'Enabled' in value['Admin'] and 'Active' in value['State'] and 'Serial' not in value['Type']:
                if value['Operation'] != 'Up' and value['Link'] != 'Up' and key != '5/3':
                    self.failed('Port {} Operation: {} Link: {} review connectivity'.format(key,value['Operation'],value['Link'],value['Pair'],value['Redundant']))
            
            if key in lac_main_ports and value['Link'] != 'Up':
                    self.failed('Port {} Operation: {} Link: {} review connectivity'.format(key,value['Operation'],value['Link'],value['Pair'],value['Redundant']))
    @aetest.test    
    def show_port_utilization_table(self, device,HC_param):
        # configure each device interface
        show_port = device.parse('show port utilization table')
        lac_main_ports= ['5/1','6/1']
        ports_rx=[]
        for key,value in show_port['port_table'].items():
            if key not in lac_main_ports:
                ports_rx.append(int(value['5min_rx']))
        median_ports=median(ports_rx)
        deviation_ports = stdev(ports_rx)
        deviation_percent = int((deviation_ports*100)/median_ports)
        if deviation_percent >= HC_param.p_dev:
            self.failed('Load Balance between ports is greather than 15% current deviation is : {}%'.format(deviation_percent))
        log.info('Load Balance current deviation is : {}%'.format(deviation_percent))
    @aetest.test    
    def show_link_aggregation_table(self, device):
        # configure each device interface
        link_agg = device.parse('show link-aggregation table')
        for key, value in link_agg['link-aggregation_table'].items():
            if 'Enabled' in value['ADMIN']:
                if 'LA+' not in value['REDUNDANT']:
                    self.failed('Error port:{} out of LAG'.format(key))

          
class SERVICES_AND_SESSIONS(aetest.Testcase):
    @aetest.test    
    def show_npu_utilization(self, device,HC_param):
        # configure each device interface
        npu_util = device.parse('show npu utilization table')
        for key,value in npu_util['npu_utilization_table'].items():
            npu=value['NPU MIN5']
            npu_value=npu.strip('%')
            if int(npu_value)>HC_param.npu_percent:
                self.failed('Error NPU value is: {} for CPU: {}'.format(value['NPU MIN5'],key)) 
    @aetest.test    
    def show_service_all(self, device):
        # configure each device interface
        
        service_all = device.parse('show service all')
        for key,value in service_all['service_all'].items():
            if 'Started' not in value['STATE']:
                self.failed('Error, service: {} in STATE: {}'.format(key,value['STATE']))    
    @aetest.test    
    def show_session_counters(self, device,HC_param):
        # configure each device interface
        session_counters = device.parse('show session counters historical all')
        counter =0
        time_reject=[]
        for key,value in session_counters['session_counters_historical_all'].items():
            if int(key)<=HC_param.num_traps:
                reject=((int(value['FAILED'])*100)/int(value['CONNECTED']))
                if reject >HC_param.reject_percent:
                    counter +=1
                    log.info('Interval {} at {} FAILED SESSION {}%'.format(key,value['TIMESTAMP'],int(reject)))
                    time_reject.append(value['TIMESTAMP'])
        if counter >=2:
            self.failed('There are Intervals with more than 10% of failed sessions at : {} '.format(time_reject))

    @aetest.test    
    def show_session_disconnect_reasons(self, device,HC_param):
        # configure each device interface
        session_counters = device.parse('show session disconnect-reasons buckets ')
        sess_deviation =0
        disconect_list = []
        for key in session_counters['show_session_disconnect-reasons_buckets'].keys():
            dis_history = []
            for value in session_counters['show_session_disconnect-reasons_buckets'][key]:
                if 'PERCENTAGE'== value:
                    dis_now= float(session_counters['show_session_disconnect-reasons_buckets'][key][value])
                elif 'PERCENTAGE' in value:
                    dis_history.append(float(session_counters['show_session_disconnect-reasons_buckets'][key][value]))
            dis_avg=mean(dis_history)
            dis_percent =0
            if dis_avg == 0 and dis_now > 0:
                dis_percent = dis_now*100
            elif dis_avg != 0 and dis_now != 0:
                dis_percent =((dis_now/dis_avg)*100)-100
            if dis_percent >=HC_param.crit_disconnect:
                self.failed('Error The follow Disconnect-Reason {} Increased {} in the last 45 min'.format(key,int(dis_percent)))
            elif dis_percent >=HC_param.soft_disconnect:    
                log.info('Disconnect Reason : {} inceased {}% in the last 45 min'.format(key,int(dis_percent)))
                sess_deviation +=1
                disconect_list.append(key)
        if sess_deviation >=HC_param.failing_disconnect:
            self.failed('Error The follow Disconnect-Reasons Increased in the last 45 min: {}'.format(disconect_list))
              
    
class GY_AND_GX(aetest.Testcase):    
    @aetest.test    
    def show_credit_control_statistics(self, device,HC_param):
        # configure each device interface
        credit_control = device.parse('show active-charging credit-control statistics')
        for key, value in credit_control['cca_info'].items():
            #print (value)
            if int(value['Assume Possitive'])>HC_param.assume_possitive:
                self.failed('Assume Possitive for CCA: {} {}'.format(key, value['Assume Possitive']))
            if value['Result Codes']:
                log.info('Result Codes for CCA: {} {}'.format(key,value['Result Codes']))

    @aetest.test    
    def show_diameters_peer_full(self, device,HC_param):
        # configure each device interface
        diameter_peers = device.parse('show diameter peers full')
        for key, value in diameter_peers['diameter_info'].items():
            if key != 'Peer Summary':
                if 'OPEN' not in value['State'] and 'Enable' in value['Admin Status']:
                    log.info('The follow Peer is Enabled but not OPEN:\n {}'.format(value))
            else:
                log.info('Peer Summary',value)
                if int(value['CLOSED'])> HC_param.diam_peers or int(value['INTERMEDIATE'])> HC_param.diam_peers:
                    self.failed('Error Peer Summary: {}'.format(value))
    @aetest.test    
    def show_ims_auth_session_summary(self, device,HC_param):
        # configure each device interface
        ims_summary = device.parse('show ims-auth sessions summary')
        for key, value in ims_summary.items():
            if int(value['fallback'])>HC_param.fallback_sessions:
                self.failed('Error Subscribers on fallback: {}'.format(value['fallback']))
            log.info('Total Subscribers ims-auth : {} subscribers in fallback {}'.format(value['total'],value['fallback']))
            
class CommonCleanup(aetest.CommonCleanup): 
    @aetest.subsection
    def disconnect_from_devices(self, device):
        # disconnect_all
        device.disconnect()

# for running as its own executable
if __name__ == '__main__':
    #testbed = testbed.load('LE.yml')
    
    result =aetest.main()
    aetest.exit_cli_code(result)