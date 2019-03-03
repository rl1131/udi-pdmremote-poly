#!/usr/bin/env python3

""" Wemo Node Server for ISY """

import sys
import socket
import logging
import polyinterface
import pywemo

LOGGER = polyinterface.LOGGER

class Control(polyinterface.Controller):
    """ Polyglot Controller for Wemo Node Server """
    def __init__(self, polyglot):
        super().__init__(polyglot)
        self.name = 'Wemo Node Server'
        self.address = 'wemons'
        self.primary = self.address
        self.subscription_registry = pywemo.SubscriptionRegistry()
        LOGGER.info('Wemo Controler Initialized')

    def start(self):
        LOGGER.info('Starting ' + self.name)
        self.discover()
        self.subscription_registry.start()

    def stop(self):
        LOGGER.info('Wemo NodeServer is stopping')
        self.subscription_registry.stop()

    def shortPoll(self):
        for node in self.nodes.values():
            node.updateInfo()

    def updateInfo(self):
        pass

    def query(self, command=None):
        for node in self.nodes:
            self.nodes[node].reportDrivers()

    def discover(self, command=None):
        devices = pywemo.discover_devices()
        for wemodev in devices:
            if wemodev.device_type == 'LightSwitch':
                LOGGER.info('Wemo LighSwitch {} found. Adding to ISY if necessary.'.format(wemodev.name))
                address = wemodev.mac.lower()
                self.addNode(WemoSwitch(self, self.address, address, wemodev.name, wemodev, self.subscription_registry))

    id = 'WEMO_CTRL'
    commands = {'DISCOVER': discover}
    drivers = [{'driver': 'ST', 'value': 1, 'uom': 2}]



class WemoSwitch(polyinterface.Node):
    """ Polyglot for Wemo Switch """
    def __init__(self, controller, primary, address, name, wemodev, subregistry=None):
        super().__init__(controller, primary, address, name)
        self.device = wemodev
        if subregistry is not None:
            self.sreg = subregistry
            subregistry.register(self.device)
            subregistry.on(wemodev, 'BinaryState', self._onchange)
        self.st = False

    def _onchange(self, wemodev, type, value):
        """ Callback for notification from the switch that the switch status changed """
        if value == '1':
            if not self.st:
                self.st = True
                self.reportCmd('DON')
                self.setDriver('ST', 1)
        else:
            if self.st:
                self.st = False
                self.reportCmd('DOF')
                self.setDriver('ST', 0)

    def _getstate(self):
        """ Query the switch's current state """
        try:
            tval = self.device.basicevent.GetBinaryState()
            rval = tval['BinaryState'] != '0'
            LOGGER.debug('_getstate for {} returned {}'.format(self.device.name, tval))
        except Exception as ex:
            LOGGER.error('Call to get status failed with exception:')
            LOGGER.error(ex)
            rval = False
        return rval

    def updateInfo(self):
        """ Get current switch status.  If it is doesn't match our
            status value then assume someone changed it remotely """
        oldst = self.st
        self.st = self._getstate()
        if self.st != oldst:
            if self.st:
                self.reportCmd('DON')
            else:
                self.reportCmd('DOF')
        newv = 1 if self.st else 0
        self.setDriver('ST', newv)

    def don(self, command=None):
        """ ISY Request the device be turned on """
        try:
            self.device.on()
            LOGGER.debug('don {} turned on'.format(self.device.name))
        except Exception as ex:
            LOGGER.debug('Call to turn switch on failed with exception:')
            LOGGER.debug(ex)
            return False
        self.st = True
        self.setDriver('ST', 1)
        return True

    def dof(self, command=None):
        """ ISY Request the device be turned off """
        try:
            self.device.off()
            LOGGER.debug('dof {} turned off'.format(self.device.name))
        except Exception as ex:
            LOGGER.debug('Call to turn switch off failed with exception:')
            LOGGER.debug(ex)
            return False
        self.st = False
        self.setDriver('ST', 0)
        return True

    def query(self, command=None):
        """ ISY Requested that we query the remote device """
        LOGGER.debug('query of {} requested'.format(self.device.name))
        self.ts = self._getstate()
        self.updateInfo()
        self.reportDrivers()
        return True

    drivers = [ {'driver': 'ST', 'value': 0, 'uom': 2} ]

    commands = {
                   'DON': don, 
                   'DOF': dof, 
                   'QUERY': query
               }

    id = 'WEMO_SWITCH'


if __name__ == "__main__":
    try:
        LOGGER.debug("Getting Poly")
        poly = polyinterface.Interface("Wemo")
        LOGGER.debug("Starting Poly")
        poly.start()
        LOGGER.debug("Getting Control")
        wemo = Control(poly)
        LOGGER.debug("Starting Control")
        wemo.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)

        
        
        
        
        
        
        
        
        
        
        
        
        
import wiringpi
from time import sleep


radio_data_pin = 17
radio_data_pin   = 17


class FanRadio:
    def __init__(self, radio_data_pin, fan_config):
        self.config = fan_config
        self.radio_data_pin = radio_data_pin
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(radio_data_pin, wiringpi.OUTPUT)
        wiringpi.digitalWrite(radio_data_pin, 0)


def radio_send_wave(wave):
    for bit in wave:
        if bit is '0':
            wiringpi.digitalWrite(self.radio_data_pin, 0)
            wiringpi.delayMicroseconds(335)
            #860
        else:
            wiringpi.digitalWrite(self.radio_data_pin, 1)
            wiringpi.delayMicroseconds(359)
            #991
    wiringpi.digitalWrite(self.radio_data_pin, 0)


def radio_send_sequence(wave, count=10):
    wiringpi.digitalWrite(self.radio_data_pin, 0)
    for x in range(count):
        radio_send_wave(wave)
        wiringpi.delayMicroseconds(14000)

def bytes2wave(bytes):
    wave = []
    for b in bytes:
        m = 0x80
        for i in range(8):
            if b & m is not 0:
                wave.append('1')
            else:
                wave.append('0')
            m = m >> 1
    return wave



    

harbor_breeze_dc_remote = {
    'off_time_us'     : 335,      # Time in microseconds of a '0' TX signal
    'on_time_us'      : 359,      # Time in microseconds of a '1' TX signal
    'resend_delay_us' : 14000,    # Time between datasets in microseconds
    'resent_count'    : 10,       # Number of datasets to send for each press of button
    'commands'        :
        {
            'airup'   : ('AirUp', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB6, 0XC9, 0X2C, 0X80 ])),
            'airdn'   : ('AirDown', bytes2wave([ 0x92, 0x49, 0x24, 0x92, 0x49, 0x24, 0xB6, 0xCB, 0x2C, 0x80 ])),
            'natup'   : ('NaturalUp', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0X92, 0X59, 0X2C, 0X80 ])),
            'natdn'   : ('NaturalDown', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0X92, 0X5B, 0X2C, 0X80 ])),
            'airup0'  : ('AirUpOff', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB6, 0XD9, 0X2C, 0X80 ])
            'airup1'  : ('AirUpSpeed1', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0X96, 0XD9, 0X2C, 0X80 ])
            'airup2'  : ('AirUpSpeed2', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB2, 0XD9, 0X2C, 0X80 ])
            'airup3'  : ('AirUpSpeed3', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0X92, 0XD9, 0X2C, 0X80 ])
            'airup4'  : ('AirUpSpeed4', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB6, 0X59, 0X2C, 0X80 ])
            'airup5'  : ('AirUpSpeed5', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0X96, 0X59, 0X2C, 0X80 ])
            'airup6'  : ('AirUpSpeed6', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB2, 0X59, 0X2C, 0X80 ])
            'airdn0'  : ('airdn0', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB6, 0XDB, 0X2C, 0X80 ])
            'airdn1'  : ('airdn1', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0X96, 0XDB, 0X2C, 0X80 ])
            'airdn2'  : ('airdn2', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB2, 0XDB, 0X2C, 0X80 ])
            'airdn3'  : ('airdn3', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0X92, 0XDB, 0X2C, 0X80 ])
            'airdn4'  : ('airdn4', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB6, 0X5B, 0X2C, 0X80 ])
            'airdn5'  : ('airdn5', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0X96, 0X5B, 0X2C, 0X80 ])
            'airdn6'  : ('airdn6', bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB2, 0X5B, 0X2C, 0X80 ])
        }
}
off_time_us = 335
on_time_us  = 359
resend_delay_us = 14000
resend_count = 10
dir_rev = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB6, 0XC9, 0X2C, 0X80 ])
rev_nat = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0X92, 0X59, 0X2C, 0X80 ])
fwd_nat = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0X92, 0X5B, 0X2C, 0X80 ])
dir_fwd = bytes2wave([ 0x92, 0x49, 0x24, 0x92, 0x49, 0x24, 0xB6, 0xCB, 0x2C, 0x80 ])
rev_0   = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB6, 0XD9, 0X2C, 0X80 ])
rev_1   = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0X96, 0XD9, 0X2C, 0X80 ])
rev_2   = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB2, 0XD9, 0X2C, 0X80 ])
rev_3   = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0X92, 0XD9, 0X2C, 0X80 ])
rev_4   = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB6, 0X59, 0X2C, 0X80 ])
rev_5   = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0X96, 0X59, 0X2C, 0X80 ])
rev_6   = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB2, 0X59, 0X2C, 0X80 ])
fwd_0   = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB6, 0XDB, 0X2C, 0X80 ])
fwd_1   = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0X96, 0XDB, 0X2C, 0X80 ])
fwd_2   = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB2, 0XDB, 0X2C, 0X80 ])
fwd_3   = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0X92, 0XDB, 0X2C, 0X80 ])
fwd_4   = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB6, 0X5B, 0X2C, 0X80 ])
fwd_5   = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0X96, 0X5B, 0X2C, 0X80 ])
fwd_6   = bytes2wave([ 0X92, 0X49, 0X24, 0X92, 0X49, 0X24, 0XB2, 0X5B, 0X2C, 0X80 ])
testd   = bytes2wave([ 0XAA, 0X55, 0X12, 0X34, 0X56, 0X78, 0X9A, 0XBC, 0XDE, 0XFF ])



# threaded_loop_active = True;
# def threaded_loop():
    # while threaded_loop_active:
        
        
        # if garage_door_left_closing:
            
        # elif garage_door_left_opening:
        # else:
            # if 
        # sleep(0.1)
        
    
    
    
    








class rffan:

    def __init__(self, command_set):


    def set_fan_speed(self, val):
        print 'set_fan_speed', val
        radio_send_sequence(self.fwd_speeds[val])
        if val is not 0:
            self.current_on_fan_speed = val
        self.fan_speed_var = val


    def fr_switch8_h_event(self, *args):
        # Ignore first event here, because for some reason on startup we get a call.
        if self.first_switch8_h_event:
            self.first_switch8_h_event = False
            return
        context = args[0]
        print 'fr_switch8_h_event', context
        if context['control'] == 'ST':
            if int(context['action']) == 0:
                self.set_fan_speed(0)
            else:
                self.set_fan_speed(self.current_on_fan_speed)


    def fr_switch8_g_event(self, *args):
        # Ignore first event here, because for some reason on startup we get a call.
        if self.first_switch8_g_event:
            self.first_switch8_g_event = False
            return
        context = args[0]
        print 'fr_switch8_g', context
        if context['control'] == 'ST':
            fsv = int(self.fan_speed_var)
            if fsv >= 0 and fsv <= 5:
                self.set_fan_speed(fsv + 1)
            elif fsv == 6:
                # Go back to one since this isn't an off switch
                self.set_fan_speed(1)
            else:
                # We should never get here, but if we do then reset to zero
                self.set_fan_speed(0)


    def fr_var_fan_speed_event(self, *args):
        context = args[0]
        print 'fr_var_fan_speed_event', context
        val = int(context['eventInfo']['var']['val'])
        if val >= 0 and val <=6:
            self.set_fan_speed(val)


