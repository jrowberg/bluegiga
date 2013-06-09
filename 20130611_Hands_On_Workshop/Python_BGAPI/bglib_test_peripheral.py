#!/usr/bin/env python

""" Bluegiga BGAPI/BGLib implementation

Changelog:
    2013-04-12 - Initial release

============================================
Bluegiga BGLib Python interface library test peripheral app
2013-04-12 by Jeff Rowberg <jeff@rowberg.net>
Updates should (hopefully) always be available at https://github.com/jrowberg/bglib

============================================
BGLib Python interface library code is placed under the MIT license
Copyright (c) 2013 Jeff Rowberg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
===============================================

"""

__author__ = "Jeff Rowberg"
__license__ = "MIT"
__version__ = "2013-04-12"
__email__ = "jeff@rowberg.net"


import bglib, serial, time, datetime

# handler to notify of an API parser timeout condition
def my_timeout(sender, args):
    # might want to try the following lines to reset, though it probably
    # wouldn't work at this point if it's already timed out:
    #ble.send_command(ser, ble.ble_cmd_system_reset(0))
    #ble.check_activity(ser, 1)
    print "BGAPI parser timed out. Make sure the BLE device is in a known/idle state."

# handler for system_boot event
def my_system_boot(sender, args):
    print "system_boot: BLE device ready (firmware: v%d.%d.%d-%d)" % (args['major'], args['minor'], args['patch'], args['build'])

    # system boot means module is in standby state
    #ble_state = BLE_STATE_STANDBY;
    # ^^^ skip above since we're going right into advertising below

    # set advertisement interval to 200-300ms, use all advertisement channels
    # (note min/max parameters are in units of 625 uSec)
    ble.ble_cmd_gap_set_adv_parameters(320, 480, 7);
    while ble.check_activity(ser): pass

    # USE THE FOLLOWING TO LET THE BLE STACK HANDLE YOUR ADVERTISEMENT PACKETS
    # ========================================================================
    # start advertising general discoverable / undirected connectable
    #ble112.ble_cmd_gap_set_mode(BGLIB_GAP_GENERAL_DISCOVERABLE, BGLIB_GAP_UNDIRECTED_CONNECTABLE);
    #while (ble112.checkActivity(1000));

    # USE THE FOLLOWING TO HANDLE YOUR OWN CUSTOM ADVERTISEMENT PACKETS
    # =================================================================

    # build custom advertisement data
    # default BLE stack value: 0201061107e4ba94c3c9b7cdb09b487a438ae55a19
    adv_data = [
        0x02, # field length
        BGLIB_GAP_AD_TYPE_FLAGS, # field type (0x01)
        BGLIB_GAP_AD_FLAG_GENERAL_DISCOVERABLE | BGLIB_GAP_AD_FLAG_BREDR_NOT_SUPPORTED, # data (0x02 | 0x04 = 0x06)
        0x11, # field length
        BGLIB_GAP_AD_TYPE_SERVICES_128BIT_ALL, # field type (0x07)
        0xe4, 0xba, 0x94, 0xc3, 0xc9, 0xb7, 0xcd, 0xb0, 0x9b, 0x48, 0x7a, 0x43, 0x8a, 0xe5, 0x5a, 0x19
    ]

    # set custom advertisement data
    ble.ble_cmd_gap_set_adv_data(0, 0x15, adv_data);
    while ble.check_activity(ser): pass

    # build custom scan response data (i.e. the Device Name value)
    # default BLE stack value: 140942474c69622055314131502033382e344e4657
    uint8 sr_data[] = {
        0x14, // field length
        BGLIB_GAP_AD_TYPE_LOCALNAME_COMPLETE, // field type
        'M', 'y', ' ', 'A', 'r', 'd', 'u', 'i', 'n', 'o', ' ', '0', '0', ':', '0', '0', ':', '0', '0'
    };

    # get BLE MAC address
    ble.ble_cmd_system_address_get()
    while ble.check_activity(ser): pass
    BGAPI_GET_RESPONSE(r0, ble_msg_system_address_get_rsp_t);

    # assign last three bytes of MAC address to ad packet friendly name (instead of 00:00:00 above)
    sr_data[13] = (r0 -> address.addr[2] / 0x10) + 48 + ((r0 -> address.addr[2] / 0x10) / 10 * 7); // MAC byte 4 10's digit
    sr_data[14] = (r0 -> address.addr[2] & 0xF)  + 48 + ((r0 -> address.addr[2] & 0xF ) / 10 * 7); // MAC byte 4 1's digit
    sr_data[16] = (r0 -> address.addr[1] / 0x10) + 48 + ((r0 -> address.addr[1] / 0x10) / 10 * 7); // MAC byte 5 10's digit
    sr_data[17] = (r0 -> address.addr[1] & 0xF)  + 48 + ((r0 -> address.addr[1] & 0xF ) / 10 * 7); // MAC byte 5 1's digit
    sr_data[19] = (r0 -> address.addr[0] / 0x10) + 48 + ((r0 -> address.addr[0] / 0x10) / 10 * 7); // MAC byte 6 10's digit
    sr_data[20] = (r0 -> address.addr[0] & 0xF)  + 48 + ((r0 -> address.addr[0] & 0xF ) / 10 * 7); // MAC byte 6 1's digit

    # set custom scan response data (i.e. the Device Name value)
    ble112.ble_cmd_gap_set_adv_data(1, 0x15, sr_data);
    while ble.check_activity(ser): pass

    # put module into discoverable/connectable mode (with user-defined advertisement data)
    ble112.ble_cmd_gap_set_mode(BGLIB_GAP_USER_DATA, BGLIB_GAP_UNDIRECTED_CONNECTABLE);
    while ble.check_activity(ser): pass

    # set state to ADVERTISING
    ble_state = BLE_STATE_ADVERTISING;

# handler for connection_status event
def my_connection_status(sender, args):
    print "connection_status: New connection"

# handler for connection_disconnected event
def my_connection_disconnected(sender, args):
    print "connection_disconnected: Disconnected"

# handler for attributes_value event
def my_attributes_value(sender, args):
    print "attributes_value: Remote client wrote new value"

def main():
    # NOTE: CHANGE THESE TO FIT YOUR TEST SYSTEM
    port_name = "com5"
    baud_rate = 38400
    packet_mode = True

    # create BGLib object
    ble = bglib.BGLib()
    ble.packet_mode = packet_mode

    # add handler for BGAPI timeout condition (hopefully won't happen)
    ble.on_timeout += my_timeout

    # add handler for the gap_scan_response event
    ble.ble_evt_system_boot += my_system_boot

    # create serial port object and flush buffers
    ser = serial.Serial(port=port_name, baudrate=baud_rate, timeout=1)
    ser.flushInput()
    ser.flushOutput()

    # let's rock and roll!
    print "========================================"
    print "BGAPI BLE peripheral script ready!"
    print "Power on or reset BLE device to proceed."
    print "========================================"

    while (1):
        # check for all incoming data (no timeout, non-blocking)
        ble.check_activity(ser)

        # don't burden the CPU
        time.sleep(0.01)

if __name__ == '__main__':
    main()
