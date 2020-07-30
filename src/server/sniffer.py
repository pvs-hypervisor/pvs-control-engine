import pcap
import struct

from binascii import hexlify
from utils.SwitchConf import *
from config import ServerConfig

class Sniffer():

    def __init__(self, iface, pktlen):
        self.pc = pcap.pcapObject()
        self.pc.open_live(iface, pktlen, 1, 0)
        self.packet_count = 0
        self.output = {}

    def recv_packet_in(self):
        self.pc.dispatch(1, self.recv_packet)
        return self.output

    def recv_packet(self, pktlen, packet_data, timestamp):
        switch_id = ord(packet_data[0])
        input_port = ord(packet_data[1])
        payload = packet_data[2:]

        switch = SwitchConf.getSwitchById(switch_id)
        if switch is not False:
            ServerConfig.print_debug("Packet {} ----------".format(self.packet_count))
            ServerConfig.print_debug("Packet-in arrived at {} from Switch {} (Switch ID = {})".format(timestamp, switch.switch_name, str(switch.switch_id)))
            ServerConfig.print_debug("Preparing to send to the control plane, switch id {}, input port {}".format(switch_id, input_port))
            # print "Raw Data: {}".format(hexlify(payload)) # we need to do it quickly
        # else:
        #    print "Error retrieving Switch ID {}".format(switch_id)

        self.output [0] = switch_id
        self.output [1] = struct.pack("Q", input_port)
        self.output [2] = payload

        self.packet_count += 1
