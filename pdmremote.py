#!/usr/bin/env python3

import sys
import socket
import logging
import polyinterface
import wiringpi

from remotedb import harbor_breeze_6_speed_dc_remote_0 as hbremote

LOGGER = polyinterface.LOGGER
LOGGER.info('PDM Remote node server running on Python version {}'.format(sys.version_info))

nodes_to_instantiate = [ ('00', 'Harbor Breeze 6 Button Remote', hbremote, 17) ]

DFON_SPEED_DEF = 3


class Control(polyinterface.Controller):
    """ Polyglot Node Server Controller for PDM Type Remote Controls """
    def __init__(self, polyglot):
        super().__init__(polyglot)
        self.name = 'PDM Remote Node Server'
        self.address = 'pdmremote'
        self.primary = self.address
        LOGGER.info('PDM Remote Controler Initialized')

    def start(self):
        LOGGER.info('Starting ' + self.name)
        self.discover()

    def stop(self):
        LOGGER.info('PDM Remote Controler node server is stopping')

    def shortPoll(self):
        for node in self.nodes.values():
            node.updateInfo()

    def updateInfo(self):
        pass

    def query(self, command=None):
        for node in self.nodes:
            self.nodes[node].reportDrivers()

    def discover(self, command=None):
        for dev in nodes_to_instantiate:
            addr = dev[0]
            name = dev[1]
            remote = dev[2]
            gpiopin = dev[3]
            if not addr in self.nodes:
                LOGGER.info('PDM Remote {} Found. Adding to ISY.'.format(name))
                self.addNode(HB6SpeedRemote(self, self.address, addr, name, remote, gpiopin))

    id = 'PDMREMOTE'
    commands = {'DISCOVER': discover}
    drivers = [{'driver': 'ST', 'value': 1, 'uom': 2}]



class PDMRemote:
    """Given an OOK (on-off-keying) Radio Transmitter connected
       to a specified GPIO pin, this module can transmit a set of
       'commands' that on the radio.  This radio can be 315MHz
       or 433MHz (or any other radio that can be turned on/off
       via a single GPIO pin).

       Typically each 'command' represents a button on a remote
       control.  For instance a ceiling fan remote.

       The commands are specified as an iterable set of On-Off time
       pairs in microseconds... thus facilitating both OOK as well
       as PDM modulation.

       See related file 'remotedb.py' for example data structure(s).
    """

    def __init__(self, remote, radio_data_pin=17):
        """ Initialize the remote control with it's commands and the GPIO
            pin on which the radio is connected
        """
        self.radio_data_pin = radio_data_pin
        self.commands = remote['symbols']
        self.resend_delay_us = remote['parms']['inter_packet_gap_us']
        self.repeat_count = remote['parms']['repeat_count']
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(radio_data_pin, wiringpi.OUTPUT)
        wiringpi.digitalWrite(radio_data_pin, 0)

    def send(self, command):
        """ Lookup the given command string in the command dictionary
            then transmit the command repeat_count times with a delay
            of resend_delay_us microseconds between each transmit.
        """
        cmd = self.commands[command]
        for x in range(self.repeat_count):
            self.radio_send_data_set(cmd, self.radio_data_pin)
            wiringpi.delayMicroseconds(self.resend_delay_us)

    @staticmethod
    def radio_send_data_set(dataset, radio_data_pin):
        """ Each tuple element in dataset specifies a transmit-duration
            and a rest-duration in microseconds.  This function walks
            through dataset and alternates between transmit and rest
            until the dataset is exhausted.
        """
        for symbol in dataset:
            hi = symbol[0]
            lo = symbol[1]
            wiringpi.digitalWrite(radio_data_pin, 1)
            wiringpi.delayMicroseconds(hi)
            wiringpi.digitalWrite(radio_data_pin, 0)
            wiringpi.delayMicroseconds(lo)



class HB6SpeedRemote(polyinterface.Node):
    """ Polyglot Node for Harbor Breeze 6 Speed Fan Remote Control """

    SUMMER = 0
    WINTER = 1
    GPIO_PIN_DEF = 17
    speedcmd = [ ('off', 'dn1', 'dn2', 'dn3', 'dn4', 'dn5', 'dn6'),
                 ('off', 'up1', 'up2', 'up3', 'up4', 'up5', 'up6') ]

    def __init__(self, controller, primary, address, name, remote, gpiopin):
        super().__init__(controller, primary, address, name)
        self.name = name
        self.st = False
        self.mode  = self.SUMMER
        self.speed = 0
        self.remotedata = remote
        self.gpiopin = gpiopin
        self.pdmremote = PDMRemote(self.remotedata, self.gpiopin)
        self.last_on_speed = 1
        self.updateInfo( )

    def updateInfo(self):
        """ Get current switch status.  If it is doesn't match our
            status value then assume someone changed it remotely """
        self.setDriver('ST', self.speed)
        self.setDriver('GV0', self.mode)
        self.setDriver('GV1', self.gpiopin)
        pass

    def _setspeed(self):
        self.pdmremote.send(self.speedcmd[self.mode][self.speed])
        self.setDriver('ST', self.speed)

    def don(self, command=None):
        """ ISY Request the device be turned on """
        if self.speed == 0:
            self.speed = self.last_on_speed
        self._setspeed()
        return True

    def dof(self, command=None):
        """ ISY Request the device be turned on """
        self.speed = 0
        self._setspeed()
        return True

    def dfon(self, command=None):
        """ ISY Request the device be turned on """
        self.speed = DFON_SPEED_DEF
        self._setspeed()
        return True

    def speedinc(self, command=None):
        """ ISY Request the device be turned on """
        if self.speed < (len(self.speedcmd[self.mode]) - 1):
            self.speed += 1
        self._setspeed()
        return True

    def speeddec(self, command=None):
        """ ISY Request the device be turned on """
        if self.speed > 0:
            self.speed -= 1
        self._setspeed()
        return True

    def query(self, command=None):
        """ ISY Requested that we query the remote device """
        LOGGER.debug('query of {} requested'.format(self.device.name))
        self.updateInfo()
        self.reportDrivers()
        return True

    def setmode(self, command=None):
        val = int(command.get('value'))
        if val:
            self.mode = self.WINTER
        else:
            self.mode = self.SUMMER
        return True

    def setspeed(self, command=None):
        val = int(command.get('value'))
        if val < len(self.speedcmd[self.mode]):
            self.speed = val
        self._setspeed()

    def setgpio(self, command=None):
        val = int(command.get('value'))
        if val <= 27:
            self.gpiopin = val
        self.pdmremote = PDMRemote(self.remotedata, self.gpiopin)

    drivers = [ {'driver': 'ST', 'value': 0, 'uom': 25},
                {'driver': 'GV0', 'value' : 0, 'uom' : 25},
                {'driver': 'GV1', 'value' : 0, 'uom' : 25}
              ]

    commands = {
                   'DON': don,
                   'DOF': dof,
                   'DFON': dfon,
                   'DFOF': dof,
                   'BRT' : speedinc,
                   'DIM' : speeddec,
                   'QUERY': query,
                   'SETSPEED' : setspeed,
                   'SETMODE' : setmode,
                   'SETGPIO' : setgpio
               }

    id = 'HB6REMOTE'


if __name__ == "__main__":
    try:
        LOGGER.debug("Getting Poly")
        poly = polyinterface.Interface("PDMRemote")
        LOGGER.debug("Starting Poly")
        poly.start()
        LOGGER.debug("Getting Control")
        pdmremote = Control(poly)
        LOGGER.debug("Starting Control")
        pdmremote.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
