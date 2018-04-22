'''
This file is part of EEWIDS 

EEWIDS is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

EEWIDS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import sys
import struct


def _parse_ssid(packet, length, offset):
    if length == 0:
        return {'ESSID': 'WILDCARD',}
    else:
        essid = (packet[offset:offset+length]).decode('utf-8', errors='replace')
        return {'ESSID': essid,} 

def _parse_country(packet, length, offset):
    code = packet[offset:offset+2].decode('ascii', errors='ignore')
    return {'country_code': code,} 

def _parse_default(packet, length, offset):
    return {} 

def parse_element_fields(packet):

    elements = {}
    offset = 12 # tagged fields

    while (offset < (len(packet)-1)):

        hdr_fmt = "<BB"
        hdr_len = struct.calcsize(hdr_fmt)
        elementID, length = struct.unpack_from(hdr_fmt, packet, offset)
        offset += hdr_len

        dispatch_table = {
                0x00: _parse_ssid,
                0x07: _parse_country,
                }

        new_elements = dispatch_table.get(elementID, _parse_default)(packet, length, offset)
        elements.update(new_elements)
        offset += length

    return elements 
