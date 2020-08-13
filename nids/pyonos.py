#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103
'''
ONOS Core REST API python client module
BASE URL: /onos/v1 , API VERSION: 1.0
'''

import json
import re
import requests

class ONOSClient():
    '''
    REST API client interface.

    Currently only works using the default URI based on the IPv4 address of the ONOS controller: http://IPv4-address:port/onos/v1
    '''

    IPV4_REGEX = re.compile(r'^(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.){3}(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d))$')
    MAC_REGEX = re.compile(r'^(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$')
    OFDEV_REGEX = re.compile(r'^of:[0-9a-fA-F]{16}$')
    APPCK_REGEX = re.compile(r'^0x[0-9a-fA-F]{8}$')

    def __init__(self, uribase: str, uriport: int, user: str, password: str):
        if uribase is None or not isinstance(uribase, str) or ONOSClient.IPV4_REGEX.match(uribase) is None:
            raise TypeError('uribase must be a string representing an IPv4 address')
        if uriport is None or not isinstance(uriport, int) or uriport < 1 or uriport > 65535:
            raise TypeError('uriport must be an integer between 1 and 65535, inclusive')
        if user is not None and not isinstance(user, str):
            raise TypeError('user must be a string')
        if password is not None and not isinstance(password, str):
            raise TypeError('password must be a string')
        if user is None:
            user = 'onos'
        if password is None:
            password = 'rocks'
        self.__url = 'http://{0:s}:{1:d}/onos/v1'.format(uribase, uriport)
        self.__auth = requests.auth.HTTPBasicAuth(user, password)

    # Basic REST methods (GET, POST, DELETE)
    def __get(self, urisuffix: str) -> dict:
        '''
        Sends a raw GET request based on the provided urisuffix.

        urisuffix must be a string representing the object to be requested with the API (e.g. '/flows/of:0000000000000001')
        '''
        if urisuffix[0] != '/':
            urisuffix = '/' + urisuffix
        headers = {'Accept': 'application/json'}
        response = requests.get(self.__url + urisuffix, headers=headers, auth=self.__auth)
        try:
            return response.json()
        except ValueError:
            return None

    def __post(self, urisuffix: str, body: dict) -> dict:
        '''
        Sends a POST request based on the provided urisuffix and body.

        urisuffix must be a string representing the object to be posted with the API and any required parameters
        (e.g. '/flows/of:0000000000000001?appId=org.onosproject.fwd')

        body must be a dictionary containing the values of the object to be posted, so that those values can be
        represented as a JSON string to be sent as a stream using the REST API.
        '''
        if body is None or not isinstance(body, dict):
            raise TypeError('body must be a dictionary with the data to be posted in the request')
        if urisuffix[0] != '/':
            urisuffix = '/' + urisuffix
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        stream = json.dumps(body)
        response = requests.post(self.__url + urisuffix, data=stream, auth=self.__auth, headers=headers)
        try:
            return response.json()
        except ValueError:
            return None

    def __delete(self, urisuffix: str, body: dict) -> dict:
        '''
        Sends a DELETE request based on the provided urisuffix and body.

        urisuffix must be a string representing the object to be deleted with the API and any required parameters
        (e.g. '/flows/of:0000000000000001?appId=org.onosproject.fwd')

        If the request requires a body, it must be a dictionary containing the values of the object to be deleted,
        so that those values can be represented as a JSON string to be sent as a stream using the REST API. If no
        body is required, it can be left as a None value and no data will be added to the request.
        '''
        if body is not None and not isinstance(body, dict):
            raise TypeError('body must be a dictionary with the data to be deleted in the request')
        if urisuffix[0] != '/':
            urisuffix = '/' + urisuffix
        if body is not None:
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            stream = json.dumps(body)
            response = requests.delete(self.__url + urisuffix, data=stream, auth=self.__auth, headers=headers)
        else:
            headers = {'Accept': 'application/json'}
            response = requests.delete(self.__url + urisuffix, auth=self.__auth, headers=headers)
        try:
            return response.json()
        except ValueError:
            return None

    # APPLICATIONS: Manage the inventory of applications
    def applications(self) -> list:
        '''
        Request an array of all installed applications.
        '''
        response = self.__get('/applications')
        if response is not None and 'applications' in response.keys():
            return response['applications']
        return None

    # DEVICES: Manage the inventory of infrastructure devices
    def devices(self) -> list:
        '''
        Request a list of the current infrastructure devices included in the inventory
        of the controller.
        '''
        response = self.__get('/devices')
        if response is not None and 'devices' in response.keys():
            return response['devices']
        return None

    def device(self, dev_id: str) -> dict:
        '''
        Request the details of the specified infrastructure device.
        '''
        if ONOSClient.OFDEV_REGEX.match(dev_id) is not None:
            response = self.__get('/devices/{0:s}'.format(dev_id.lower()))
            return response
        else:
            raise TypeError('devId must be a string representing a valid infrastructure device ID.')

    def devicePorts(self, dev_id: str) -> list:
        '''
        Request the details of the ports associated with the specified infrastructure device.
        '''
        if ONOSClient.OFDEV_REGEX.match(dev_id) is not None:
            response = self.__get('/devices/{0:s}/ports'.format(dev_id.lower()))
            if 'ports' in response.keys():
                return response['ports']
            return None
        else:
            raise TypeError('devId must be a string representing a valid infrastructure device ID.')

    def delDevice(self, dev_id: str) -> dict:
        '''
        Administratively delete the specified device from the inventory of known devices.
        '''
        if ONOSClient.OFDEV_REGEX.match(dev_id) is not None:
            return self.__delete('/devices/{0:s}'.format(dev_id.lower()), None)
        else:
            raise TypeError('devId must be a string representing a valid infrastructure device ID.')

    # FLOWS: Query and program flow rules
    def flows(self) -> list:
        '''
        Request a list with all the flow rules in the system.
        '''
        response = self.__get('/flows')
        if 'flows' in response.keys():
            return response['flows']
        return None

    def appFlows(self, app_id: str) -> list:
        '''
        Request a list with all the flow rules specified by the given application.
        '''
        if app_id is None or not isinstance(app_id, str) or re.search(r'\s', app_id) is not None:
            raise TypeError('appId must be a valid application id.')
        response = self.__get('/flows/application/{0:s}'.format(app_id))
        if 'flows' in response.keys():
            return response['flows']
        return None

    def deviceFlows(self, dev_id: str) -> list:
        '''
        Request a list of all the flow rules for the specified device.
        '''
        if ONOSClient.OFDEV_REGEX.match(dev_id) is not None:
            response = self.__get('/flows/{0:s}'.format(dev_id.lower()))
            if 'flows' in response.keys():
                return response['flows']
            return None
        else:
            raise TypeError('devId must be a string representing a valid infrastructure device ID.')

    def flowRule(self, dev_id: str, flow_id: int) -> dict:
        '''
        Request the details of a particular flow rule in a specified device.
        '''
        if ONOSClient.OFDEV_REGEX.match(dev_id) is None:
            raise TypeError('devId must be a string representing a valid infrastructure device ID.')
        if flow_id is None or not isinstance(flow_id, int):
            raise TypeError('flowId must be an integer representing a valid flow rule ID.')
        response = self.__get('/flows/{0:s}/{1:d}'.format(dev_id.lower(), flow_id))
        if 'flows' in response.keys():
            response = response['flows']
            if response:
                return response[0]
        return None

    def pendingFlows(self) -> list:
        '''
        Request a list of all the pending flow rules in the system.
        '''
        response = self.__get('/flows/pending')
        if 'flows' in response.keys():
            return response['flows']
        return None

    def addFlows(self, app_id: str, flows: dict) -> dict:
        '''
        Create the specified flow rules.
        '''
        if app_id is None or not isinstance(app_id, str) or re.search(r'\s', app_id) is not None:
            raise TypeError('appId must be a valid application id.')
        if flows is None or not isinstance(flows, dict):
            raise TypeError('flows must be a dictionary containing the data structure of the new flow rules.')
        return self.__post('/flows?=appId={0:s}'.format(app_id.lower()), flows)

    def addFlow(self, dev_id: str, app_id: str, flow: dict) -> dict:
        '''
        Create the given flow rule in the specified device.
        '''
        if ONOSClient.OFDEV_REGEX.match(dev_id) is None:
            raise TypeError('devId must be a string representing a valid infrastructure device ID.')
        if app_id is None or not isinstance(app_id, str) or re.search(r'\s', app_id) is not None:
            raise TypeError('appId must be a valid application id.')
        if flow is None or not isinstance(flow, dict):
            raise TypeError('flow must be a dictionary containing the data structure of the new flow rule.')
        return self.__post('/flows/{0:s}?appId={1:s}'.format(dev_id.lower(), app_id.lower()), flow)

    def delFlow(self, dev_id: str, flow_id: int) -> dict:
        '''
        Delete the specified flow rule from the given device
        '''
        if ONOSClient.OFDEV_REGEX.match(dev_id) is None:
            raise TypeError('devId must be a string representing a valid infrastructure device ID.')
        if flow_id is None or not isinstance(flow_id, int):
            raise TypeError('flowId must be an integer representing a valid flow rule ID.')
        return self.__delete('/flows/{0:s}/{1:d}'.format(dev_id.lower(), flow_id), None)

    def delAppFlows(self, app_id: str) -> dict:
        '''
        Delete all the flow rules associated with the given application
        '''
        if app_id is None or not isinstance(app_id, str) or re.search(r'\s', app_id) is not None:
            raise TypeError('appId must be a valid application id.')
        return self.__delete('/flows/application/{0:s}'.format(app_id.lower()), None)

    # GROUPS: Query and program group rules
    def groups(self) -> list:
        '''
        Request a list of all groups currently stored in the inventory
        '''
        response = self.__get('/groups')
        if 'groups' in response.keys():
            return response['groups']
        return None

    def deviceGroups(self, dev_id: str) -> list:
        '''
        Request a list of all the groups associated with the specified device
        '''
        if dev_id is None or not isinstance(dev_id, str) or ONOSClient.OFDEV_REGEX.match(dev_id) is not None:
            response = self.__get('/groups/{0:s}'.format(dev_id.lower()))
            if 'groups' in response.keys():
                return response['groups']
            return None
        else:
            raise TypeError('devId must be a string representing a valid infrastructure device ID.')

    def addGroup(self, dev_id: str, group: dict) -> dict:
        '''
        Create a new group rule in the specified device
        '''
        if dev_id is None or not isinstance(dev_id, str) or ONOSClient.OFDEV_REGEX.match(dev_id) is None:
            raise TypeError('devId must be a string representing a valid infrastructure device ID.')
        if group is None or not isinstance(group, dict):
            raise TypeError('group must be a dictionary containing the data structure of the new group.')
        return self.__post('/groups/{0:s}'.format(dev_id.lower()), group)

    def addBuckets(self, dev_id: str, app_cookie: str, buckets: dict) -> dict:
        '''
        Adds buckets to an existing group in a specified device
        '''
        if dev_id is None or not isinstance(dev_id, str) or ONOSClient.OFDEV_REGEX.match(dev_id) is None:
            raise TypeError('devId must be a string representing a valid infrastructure device ID.')
        if app_cookie is None or not isinstance(app_cookie, str) or ONOSClient.APPCK_REGEX.match(app_cookie) is None:
            raise TypeError('appCookie must be a string representing a valid application cookie.')
        if buckets is None or not isinstance(buckets, dict):
            raise TypeError('buckets must be a dictionary containing the data structure of the new buckets.')
        return self.__post('/groups/{0:s}/{1:d}/buckets'.format(dev_id.lower(), app_cookie.lower()), buckets)

    def delBuckets(self, dev_id: str, app_cookie: str, bucket_ids: list) -> dict:
        '''
        Delete the specified buckets from the specified group from a given device
        '''
        if dev_id is None or not isinstance(dev_id, str) or ONOSClient.OFDEV_REGEX.match(dev_id) is None:
            raise TypeError('devId must be a string representing a valid infrastructure device ID.')
        if app_cookie is None or not isinstance(app_cookie, str) or ONOSClient.APPCK_REGEX.match(app_cookie) is None:
            raise TypeError('appCookie must be a string representing a valid application cookie.')
        if bucket_ids is None or not isinstance(bucket_ids, list) or any(not isinstance(bucket, int) for bucket in bucket_ids):
            raise TypeError('bucketIds must be a list containing the integer IDs of the buckets to be deleted.')
        ids = ','.join(str(b) for b in bucket_ids)
        return self.__delete('/groups/{0:s}/{1:s}/buckets/{2:s}'.format(dev_id.lower(), app_cookie.lower(), ids), None)

    def delGroup(self, dev_id: str, app_cookie: str) -> dict:
        '''
        Delete the specified group having the provided appCookie from a given device
        '''
        if dev_id is None or not isinstance(dev_id, str) or ONOSClient.OFDEV_REGEX.match(dev_id) is None:
            raise TypeError('devId must be a string representing a valid infrastructure device ID.')
        if app_cookie is None or not isinstance(app_cookie, str) or ONOSClient.APPCK_REGEX.match(app_cookie) is None:
            raise TypeError('appCookie must be a string representing a valid application cookie.')
        return self.__delete('/groups/{0:s}/{1:s}'.format(dev_id.lower(), app_cookie.lower()), None)

    def getGroup(self, dev_id: str, app_cookie: str) -> dict:
        '''
        Request the details of a group given the device ID and the application cookie.
        '''
        if dev_id is None or not isinstance(dev_id, str) or ONOSClient.OFDEV_REGEX.match(dev_id) is None:
            raise TypeError('devId must be a string representing a valid infrastructure device ID.')
        if app_cookie is None or not isinstance(app_cookie, str) or ONOSClient.APPCK_REGEX.match(app_cookie) is None:
            raise TypeError('appCookie must be a string representing a valid application cookie.')
        return self.__get('/groups/{0:s}/{1:s}'.format(dev_id.lower(), app_cookie.lower()))

    # HOSTS: Query the inventory of end-station hosts
    def hosts(self) -> list:
        '''
        Request a list of the currently known end-station hosts included in the inventory
        of the controller
        '''
        response = self.__get('/hosts')
        if response is not None and 'hosts' in response.keys():
            return response['hosts']
        return None

    def host(self, mac: str, vlan: int) -> dict:
        '''
        Request the detailed propoerties of the specified end-station host.
        '''
        if mac is None or not isinstance(mac, str) or ONOSClient.MAC_REGEX.match(mac) is None:
            raise TypeError('mac must be a string representing a MAC address of a host device')
        if vlan is not None and (not isinstance(vlan, int) or (vlan > 4094 or vlan < 1)):
            raise ValueError('vlan must be an integer between 1 and 4094, inclusive')
        elif vlan is not None:
            response = self.__get('/hosts/{0:s}/{1:d}'.format(mac, vlan))
        else:
            response = self.__get('/hosts/{0:s}/None'.format(mac))
        return response

    # LINKS: Query the inventory of infrastructure links
    def links(self, dev_id: str) -> list:
        '''
        Request a list of the infrastructure links currently stored in the inventory.

        Optionally, a device ID can be specified to request the links associated with
        the specified infrastructure device.
        '''
        if dev_id is None:
            response = self.__get('/links')
        elif isinstance(dev_id, str) and ONOSClient.OFDEV_REGEX.match(dev_id) is not None:
            response = self.__get('/links?device={0:s}'.format(dev_id.lower()))
        else:
            raise TypeError('devId must be a string representing a valid infrastructure device ID.')
        if 'links' in response.keys():
            return response['links']
        return None

if __name__ == '__main__':
    import code
    import readline
    import rlcompleter
    CONTEXT = globals()
    CONTEXT = CONTEXT.copy()
    CONTEXT.update(locals())
    readline.set_completer(rlcompleter.Completer(CONTEXT).complete)
    readline.parse_and_bind('tab: complete')
    SHELL = code.InteractiveConsole(CONTEXT)
    SHELL.interact()
