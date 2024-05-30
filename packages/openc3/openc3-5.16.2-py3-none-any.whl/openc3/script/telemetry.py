# Copyright 2022 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addums as found in the LICENSE.txt

# Modified by OpenC3, Inc.
# All changes Copyright 2023, OpenC3, Inc.
# All Rights Reserved
#
# This file may also be used under the terms of a commercial license
# if purchased from OpenC3, Inc.

import time
import openc3.script
from openc3.script.api_shared import openc3_script_sleep
from openc3.environment import OPENC3_SCOPE


# Get packets based on ID returned from subscribe_packet.
# @param id [String] ID returned from subscribe_packets or last call to get_packets
# @param block [Float] Time in seconds to wait for packets to be received
# @param block_delay [Float] Time in seconds to sleep between polls
# @param count [Integer] Maximum number of packets to return from EACH packet stream
# @return [Array<String, Array<Hash>] Array of the ID and array of all packets found
def get_packets(id, block=None, block_delay=0.1, count=1000, scope=OPENC3_SCOPE):
    start_time = time.time()
    if block:
        _time = start_time + block
    while True:
        id, packets = getattr(openc3.script.API_SERVER, "get_packets")(id, count=count, scope=scope)
        if block and time.time() < _time and not packets:
            openc3_script_sleep(block_delay)
        else:
            break
    return id, packets


# inject_tlm, set_tlm, override_tlm, and normalize_tlm are implemented here simply to add a print
# these methods modify the telemetry so the user should be notified in the Script Runner log messages


def inject_tlm(target_name, packet_name, item_hash=None, type="CONVERTED", scope=OPENC3_SCOPE):
    print(f'inject_tlm("{target_name}", "{packet_name}", {item_hash}, type="{type}")')
    getattr(openc3.script.API_SERVER, "inject_tlm")(target_name, packet_name, item_hash, type=type, scope=scope)


def set_tlm(*args, type="CONVERTED", scope=OPENC3_SCOPE):
    if len(args) == 1:
        print(f'set_tlm("{args[0]}", type="{type}")')
    else:
        if isinstance(args[3], str):
            value = f'"{args[3]}"'
        else:
            value = args[3]
        print(f'set_tlm("{args[0]}", "{args[1]}", "{args[2]}", {value}, type="{type}")')
    getattr(openc3.script.API_SERVER, "set_tlm")(*args, type=type, scope=scope)


def override_tlm(*args, type="ALL", scope=OPENC3_SCOPE):
    if len(args) == 1:
        print(f'override_tlm("{args[0]}", type="{type}")')
    else:
        if isinstance(args[3], str):
            value = f'"{args[3]}"'
        else:
            value = args[3]
        print(f'override_tlm("{args[0]}", "{args[1]}", "{args[2]}", {value}, type="{type}")')
    getattr(openc3.script.API_SERVER, "override_tlm")(*args, type=type, scope=scope)


def normalize_tlm(*args, type="ALL", scope=OPENC3_SCOPE):
    if len(args) == 1:
        print(f'normalize_tlm("{args[0]}", type="{type}")')
    else:
        if isinstance(args[3], str):
            value = f'"{args[3]}"'
        else:
            value = args[3]
        print(f'normalize_tlm("{args[0]}", "{args[1]}", "{args[2]}", {value}, type="{type}")')
    getattr(openc3.script.API_SERVER, "normalize_tlm")(*args, type=type, scope=scope)
