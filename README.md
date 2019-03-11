# Polyglot v2 Node Server for PDM/OOK Modulated Remote Controls

NOTE: THIS IS A WORK IN PROGRESS and not yet ready

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/rl1131/udi-wemo-poly/blob/master/LICENSE)

### Overview

This [Polyglot v2](https://github.com/UniversalDevicesInc/polyglot-v2) node 
server provides an interface between the ISY home automation controller from 
Universal Devices Inc. and RF Controlled Ceiling fans.

Many remote controls out in the wild use a basic form of modulation
called OOK or PDM to control their respective devices.  Most RF controlled
ceiling 

These fans tend to have very similar RF codes.  So, you may get
this node server to work with other fans.  At some point I'll
create a How-To page for reverse engineering the codes which can
then be easily added to this node server.

### Installation instructions

You can install this node server by manually running
```
cd ~/.polyglot/nodeservers
git clone https://github.com/rl1131/udi-pdmremote-poly.git udi-pdmremote-poly
cd udi-pdmremote-poly
./install.sh
```

After that is complete use the Polyglot web interface to add the node server.

### Currently Supported Device(s)

Harbor Breeze 6 Speed Fan Remote Control
![HB6Speed](https://user-images.githubusercontent.com/11381527/54090368-d99dcf00-4330-11e9-9670-c33772a9025e.jpg)

### Hardware

It is required that a 315 MHz transmitter be connected to the Raspberry Pi that is running this node server.

These transmitters (along with a receiver) are available on Amazon for about $5 shipped (or $0.73 each from aliexpress.com).  Only the transmitter is needed for this project... the receiver is not used.

[315MHz Transmitter](https://www.amazon.com/HiLetgo-Transmitter-Receiver-Arduino-Raspberry/dp/B00LNADJS6/)

First solder an antenna to the transmitter.  A length of wire that is about 8.9 inches long.

Connect the transmitter to the Raspberry Pi using the pinout (see photos and GPIO pinout):

![radioconnecttable](https://user-images.githubusercontent.com/11381527/53689792-78fc0a00-3d12-11e9-8186-21fd6b45ef95.jpg)

![ThesePins](https://user-images.githubusercontent.com/11381527/53689718-8d3f0780-3d10-11e9-8e1c-abe836bb3e29.jpg)

![RadioBoard](https://user-images.githubusercontent.com/11381527/53689699-47823f00-3d10-11e9-8c1d-dd774befb156.jpg)

![RPiWithRadioBoard](https://user-images.githubusercontent.com/11381527/53689705-5ff25980-3d10-11e9-902d-93bbc9c80f0c.jpg)

![RPiPinsForRadio](https://user-images.githubusercontent.com/11381527/53689713-7b5d6480-3d10-11e9-877a-48be32d681ba.jpg)

