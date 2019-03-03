# Polyglot v2 Node Server for RF Fan Control of Harbor Breeze Fan

NOTE: THIS IS A WORK IN PROGRESS and not yet ready

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/rl1131/udi-wemo-poly/blob/master/LICENSE)

### 

This version of this node server provides most of the functionality of the remote control shown at the bottom of this page.

![RemoteFront](https://user-images.githubusercontent.com/11381527/53689078-798ca480-3d02-11e9-8911-456f7b8fbbf2.jpg)
![RemoteBack](https://user-images.githubusercontent.com/11381527/53689081-8ad5b100-3d02-11e9-9a47-622d836fce09.jpg)

This [Polyglot v2](https://github.com/UniversalDevicesInc/polyglot-v2) node server provides an interface between the ISY home automation controller from Universal Devices Inc. and RF Controlled Ceiling fans.

These fans tend to have very similar RF codes.  So, you may get
this node server to work with other fans.  At some point I'll
create a How-To page for reverse engineering the codes which can
then be easily added to this node server.

### Installation instructions

You can install this node server by manually running
```
cd ~/.polyglot/nodeservers
git clone https://github.com/rl1131/udi-rffans-poly.git udi-rffans-poly
cd udi-rffans-poly
./install.sh
```

After that is complete use the Polyglot web interface to add the node server.

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

