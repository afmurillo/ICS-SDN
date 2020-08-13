#!/usr/bin/env python3
'''
Web UI for the ICS SDN-based IDS.
'''

import os
import sys
import json
import base64
import threading
import signal
import time
import collections
import netaddr
import cherrypy
import sdnids
import pyonos

class MissingArgumentException(Exception):
    '''Simple exception to indicate missing arguments'''
    pass

class SnifferHandler(threading.Thread):
    '''
    Handles the interaction with the sniffer component of the IDS.
    Receives relevant data from the analyzed traffic.
    '''

    def __init__(self, iface: str, parent):
        threading.Thread.__init__(self)
        self.__parent = parent
        self.__buffer = collections.deque(iterable=[], maxlen=65536)
        self.__sniffer = sdnids.ICSSniffer(interface=iface)
        self.should_stop = threading.Event()
        self.__pps = 0

    def sniffed_stats(self) -> collections.OrderedDict:
        '''
        Get the current stats from the sniffer.
        '''
        return self.__sniffer.get_stats()

    def run(self):
        self.__sniffer.start()
        while not self.should_stop.is_set():
            self.__buffer.clear()
            self.__pps = self.__sniffer.size()
            i = self.__pps
            enip = 0
            while i > 0:
                curr_msg = self.__sniffer.pop()
                if curr_msg['is_enip']:
                    enip += 1
                self.__buffer.append(curr_msg)
                i -= 1
            self.__parent.push_hpps([time.time(), self.__pps, enip])
            time.sleep(1)
        cherrypy.log(msg='Handler stopped. Sending stop signal to sniffer ...', context='SNIFFER HANDLER')
        self.__sniffer.should_stop.set()
        cherrypy.log(msg='Waiting for sniffer to end ...', context='SNIFFER HANDLER')
        while self.__sniffer.is_alive():
            self.__sniffer.join(1)
        cherrypy.log(msg='Sniffer stopped.', context='SNIFFER HANDLER')

class MainApp():
    '''
    Main class of the web UI.
    Implements the necessary actions to take for each HTTP request.
    '''

    def __init__(self, **kwargs):
        if any(kw not in ['idsconfig', 'onosip', 'onosport', 'onosuser', 'onospass', 'idsiface'] for kw in kwargs.keys()): # pylint: disable=C0201
            raise MissingArgumentException
        idsconfig = kwargs.pop('idsconfig')
        onosip = kwargs.pop('onosip')
        onosport = kwargs.pop('onosport')
        onosuser = kwargs.pop('onosuser')
        onospass = kwargs.pop('onospass')
        idsiface = kwargs.pop('idsiface')
        iconf = open(idsconfig, 'r').read()
        self.__i_path = idsconfig
        self.__i_conf = json.loads(iconf)
        self.__h_pps = collections.deque(iterable=[], maxlen=600)
        self.__onos = pyonos.ONOSClient(onosip, onosport, onosuser, onospass)
        self.__s_handler = SnifferHandler(idsiface, self)
        self.__s_handler.start()

    def push_hpps(self, data: list):
        '''
        Append sniffer stats to the local stats buffer. (max: 10 minutes --600 seconds--)
        '''
        self.__h_pps.append(data)

    @cherrypy.expose
    def index(self):
        '''
        Return the main index template.
        '''
        return open('webui/templates/index.html', 'r').read()

    @cherrypy.expose
    def reloadconfig(self):
        '''
        Reload the configureation file as needed.
        '''
        iconf = open(self.__i_path, 'r').read()
        self.__i_conf = json.loads(iconf)
        return 'OK'

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getappids(self):
        '''
        Return the active apps installed on the configured SDN controller.
        '''
        apps = self.__onos.applications()
        appids = []
        for app in apps:
            if isinstance(app, dict) and 'state' in app.keys() and app['state'] == 'ACTIVE':
                appids.append(app['name'])
        return {'appids': sorted(appids)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getdevices(self):
        '''
        Retrieve the SDN devices currently included in the SDN controller's inventory.
        '''
        devices = self.__onos.devices()
        if 'devroles' not in self.__i_conf:
            self.__i_conf['devroles'] = {}
        spports = {}
        if 'span' in self.__i_conf['devroles'].values():
            for dev in devices:
                if self.__i_conf['devroles'][dev['id']] == 'span':
                    for slink in self.__onos.links(dev_id=dev['id']):
                        if slink['src']['device'] == dev['id']:
                            spports[slink['dst']['device']] = int(slink['dst']['port'])
                        else:
                            spports[slink['src']['device']] = int(slink['src']['port'])
                    break
        for i in range(len(devices)): # pylint: disable=C0200
            dev = devices[i]
            if dev['id'] not in spports.keys():
                spports[dev['id']] = -1
            if dev['id'] in self.__i_conf['devroles']:
                dev['role'] = self.__i_conf['devroles'][dev['id']]
            else:
                dev['role'] = 'na'
            if 'span' in self.__i_conf['devroles'].values():
                if dev['role'] == 'span':
                    dev['spanport'] = 0
                else:
                    dev['spanport'] = spports[dev['id']]
            else:
                dev['spanport'] = -1
            devices[i] = dev
        devices = sorted(devices, key=lambda x: x['id'])
        return {'devs': devices}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def gethosts(self):
        '''
        Retrieve the hosts currently included in the SDN controller's inventory.
        '''
        hosts = self.__onos.hosts()
        if 'IP' not in self.__i_conf.keys():
            self.__i_conf['IP'] = {}
        if 'hostroles' not in self.__i_conf.keys():
            self.__i_conf['hostroles'] = {}
        for i in range(len(hosts)): # pylint: disable=C0200
            hst = hosts[i]
            if hst['ipAddresses'][0] in self.__i_conf['IP'].values():
                for ip_addr in self.__i_conf['IP']:
                    if self.__i_conf['IP'][ip_addr] == hst['ipAddresses'][0]:
                        hst['name'] = ip_addr
                        break
            else:
                hst['name'] = '*** UNKNOWN ***'
            if hst['mac'] in self.__i_conf['hostroles'].keys():
                hst['role'] = self.__i_conf['hostroles'][hst['mac']]
            else:
                hst['role'] = 'na'
            mac = netaddr.EUI(hst['mac'])
            try:
                oui = mac.oui
                oui = oui.registration()
                hst['mac'] += ' ({0:s})'.format(oui['org'])
            except netaddr.core.NotRegisteredError:
                hst['mac'] += ' (UNKNOWN)'
            hosts[i] = hst
        hosts = sorted(hosts, key=lambda x: x['ipAddresses'][0])
        return {'hosts': hosts}

    @cherrypy.expose
    def updatehostname(self, **kwargs):
        '''
        Rename a host within the configuration.
        '''
        if any(kw not in kwargs.keys() for kw in ['ip', 'name']):
            raise cherrypy.HTTPError(status=400, message='Missing parameters')
        else:
            ip_addr = kwargs.pop('ip')
            name = kwargs.pop('name')
            pname = None
            if 'IP' not in self.__i_conf.keys():
                self.__i_conf['IP'] = {}
            for i in self.__i_conf['IP']:
                if self.__i_conf['IP'][i] == ip_addr:
                    pname = i
                    break
            if pname is not None:
                self.__i_conf['IP'].pop(pname)
            self.__i_conf['IP'][name] = ip_addr
            json.dump(self.__i_conf, open(self.__i_path, 'w'), indent='  ')
            return 'OK'

    @cherrypy.expose
    def updatedevrole(self, **kwargs):
        '''
        Update the role of a device within the configuration.
        '''
        if any(kw not in kwargs.keys() for kw in ['id', 'role']):
            raise cherrypy.HTTPError(status=400, message='Missing parameters')
        else:
            dev_id = kwargs.pop('id')
            role = kwargs.pop('role')
            if role not in ['bridge', 'field', 'honeypot', 'span']:
                raise cherrypy.HTTPError(status=400, message='Invalid role')
            else:
                if 'devroles' not in self.__i_conf:
                    self.__i_conf['devroles'] = {}
                if role == 'span' and role in self.__i_conf['devroles'].values():
                    raise cherrypy.HTTPError(status=503, message='Mirroring device already assigned')
                self.__i_conf['devroles'][dev_id] = role
                json.dump(self.__i_conf, open(self.__i_path, 'w'), indent='  ')
                return 'OK'

    @cherrypy.expose
    def updatehostrole(self, **kwargs):
        '''
        Update a host's role within the configuration.
        '''
        if any(kw not in kwargs.keys() for kw in ['mac', 'role']):
            raise cherrypy.HTTPError(status=400, message='Missing parameters')
        else:
            mac = kwargs.pop('mac')
            role = kwargs.pop('role')
            if role not in ['plc', 'sensor', 'actuator', 'hmi']:
                raise cherrypy.HTTPError(status=400, message='Invalid role')
            else:
                if 'hostroles' not in self.__i_conf.keys():
                    self.__i_conf['hostroles'] = {}
                self.__i_conf['hostroles'][mac] = role
                json.dump(self.__i_conf, open(self.__i_path, 'w'), indent='  ')
                return 'OK'

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getppsdata(self):
        '''
        Retrieve the sniffer history buffer.
        '''
        return {'pps': list(self.__h_pps)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def gettopsniffed(self):
        '''
        Retrieve the sniffer stats.
        '''
        stats = self.__s_handler.sniffed_stats()
        s_keys = list(stats.keys())
        s_iter = 10
        while s_iter < len(s_keys):
            stats.pop(s_keys[s_iter])
            s_iter += 1
        return {'top': stats}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getdevicegroups(self, **kwargs):
        '''
        Retrieve the SDN groups of a specified device.
        '''
        if any(kw not in kwargs.keys() for kw in ['devid']):
            raise cherrypy.HTTPError(status=400, message='Missing parameters')
        else:
            devid = kwargs.pop('devid')
            groups = self.__onos.deviceGroups(devid)
            groups = sorted(groups, key=lambda x: x['id'])
        return {'groups': groups}

    @cherrypy.expose
    def creategroup(self, **kwargs):
        '''
        Create a new SDN group for a specified device.
        '''
        if any(kw not in kwargs.keys() for kw in ['devid', 'grpid', 'appck', 'buckets']):
            raise cherrypy.HTTPError(status=400, message='Missing parameters')
        params = {}
        params['devid'] = kwargs.pop('devid')
        params['grpid'] = kwargs.pop('grpid')
        params['appck'] = kwargs.pop('appck')
        params['buckets'] = json.loads(base64.b64decode(kwargs.pop('buckets')).decode('utf-8'))
        group = {
            'type': 'ALL',
            'appCookie': params['appck'],
            'groupId': params['grpid'],
            'buckets': [],
        }
        for buck in params['buckets']:
            newb = {'treatment': {'instructions': buck}}
            group['buckets'].append(newb)
        self.__onos.addGroup(params['devid'], group)
        return json.dumps(group)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def deletegroup(self, **kwargs):
        '''
        Delete a specific group from a given device.
        '''
        if any(kw not in kwargs.keys() for kw in ['devid', 'appck']):
            raise cherrypy.HTTPError(status=400, message='Missing parameters')
        devid = kwargs.pop('devid')
        appck = kwargs.pop('appck')
        rsp = self.__onos.delGroup(devid, appck)
        return {'response': rsp}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getdeviceflows(self, **kwargs):
        '''
        Retrieve the flow within a given device.
        '''
        if any(kw not in kwargs.keys() for kw in ['devid']):
            raise cherrypy.HTTPError(status=400, message='Missing parameters')
        devid = kwargs.pop('devid')
        flows = self.__onos.deviceFlows(devid)
        if flows:
            flows = sorted(flows, key=lambda x: x['priority'], reverse=True)
            return {'flows': flows}
        return None

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def createflow(self, **kwargs):
        '''
        Create a new flow within a given device.
        '''
        if 'flow' not in kwargs.keys():
            raise cherrypy.HTTPError(status=400, message='Missing parameters')
        flow = json.loads(base64.b64decode(kwargs.pop('flow')).decode('utf-8'))
        return self.__onos.addFlow(flow['deviceId'], flow['appId'], flow)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def deleteflow(self, **kwargs):
        '''
        Delete a specific flow from a given device.
        '''
        if any(kw not in kwargs.keys() for kw in ['devid', 'flowid']):
            raise cherrypy.HTTPError(status=400, message='Missing parameters')
        devid = kwargs.pop('devid')
        flowid = kwargs.pop('flowid')
        rsp = self.__onos.delFlow(devid, int(flowid))
        return {'response': rsp}

    def end_app(self):
        '''
        Gracefully terminate the web UI app.
        '''
        cherrypy.log(msg='Signaling the sniffer handler to stop ...', context='WEBUI')
        self.__s_handler.should_stop.set()
        cherrypy.log(msg='Waiting for the sniffer handler to stop ...', context='WEBUI')
        while self.__s_handler.is_alive():
            self.__s_handler.join(1)

class StopAppException(Exception):
    '''Used to signal app termination'''
    pass

def stop_app(signum: int, frame):
    '''Raise an exception that forces the threads to gracefully stop'''
    if frame is not None:
        cherrypy.log(msg='Received signal {0:d} (frame: {1:s})'.format(signum, str(type(frame))), context='ENGINE')
    else:
        cherrypy.log(msg='Received signal {0:d}'.format(signum), context='ENGINE')
    raise StopAppException

def main():
    '''Main of the entire web ui app'''
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
            'tools.sessions.storage_path': 'webui/sessions',
            'tools.sessions.timeout': 60,
            'tools.sessions.secure': True,
            'tools.sessions.httponly': True,
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath(os.path.join(os.path.dirname(__file__), 'webui/static')),
        },
        '/favicon.ico': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.abspath(os.path.join(os.path.dirname(__file__), 'webui/static/favicon.ico')),
        }
    }
    global_conf = {
        'server.socket_port': 9999,
        'log.access_file': 'webui/logs/access.log',
        'log.error_file': 'webui/logs/error.log',
    }
    signal.signal(signal.SIGTERM, stop_app)
    signal.signal(signal.SIGHUP, stop_app)
    signal.signal(signal.SIGINT, stop_app)
    signal.signal(signal.SIGUSR1, stop_app)
    try:
        cherrypy.config.update(global_conf)
        application = MainApp(
            idsconfig='sdnconfig.json',
            idsiface='att2',
            onosip='192.168.56.50',
            onosport=8181,
            onosuser='onos',
            onospass='rocks'
        )
        cherrypy.tree.mount(application, '/', conf)
        cherrypy.engine.signals.subscribe()                     # Receive signals from the OS
        cherrypy.engine.subscribe('stop', application.end_app)   # Bind the graceful stop of the custom threads (the sniffer handler and the actual sniffer
        cherrypy.engine.start()
        cherrypy.engine.block()
    except MissingArgumentException:
        print('Internal error: Missing arguments')
        sys.exit(1)
    except StopAppException:
        application.end_app()
        cherrypy.engine.exit()

if __name__ == '__main__':
    if os.geteuid() != 0:
        print('SDN IDS requires root privileges')
    else:
        main()
