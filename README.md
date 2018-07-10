# eufy-adapter

Eufy smart plug/bulb adapter for Mozilla IoT Gateway.

# Supported Devices

## Tested and Working

* Smart plugs
    * Smart Plug Mini
* Smart bulbs
    * Lumos Smart Bulb - White &amp; Color

## Untested but _Should Work_

* Smart plugs
    * Smart Plug
* Smart bulbs
    * Lumos Smart Bulb - Tunable
    * Lumos Smart Bulb - White
* Smart switches
    * Smart Switch

# Requirements

If you're running this add-on outside of the official gateway image for the Raspberry Pi, i.e. you're running on a development machine, you'll need to do the following (adapt as necessary for non-Ubuntu/Debian):

```
sudo apt install python3-dev libnanomsg-dev
sudo pip3 install nnpy
sudo pip3 install git+https://github.com/mozilla-iot/gateway-addon-python.git
```
