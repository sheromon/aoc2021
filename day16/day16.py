import operator
from pathlib import Path

import numpy as np


def day16a(input_str):
    """Return the sum of the versions of the packets and sub-packets."""
    if Path(input_str).is_file():
        with open(input_str) as file_obj:
            input_str = file_obj.readline().strip()
    vals = [int(char, base=16) for char in input_str]
    bin_str = ''.join(format(val, '04b') for val in vals)
    packets = parse(bin_str)
    val = sum(packet['version'] for packet in packets)
    return val


def parse(bin_str, process=False):
    """Parse packets and sub-packets according to complicated rules.

    :param process: bool, optional; if True, process operator packets to get a
        resulting value; if False, return the raw sub-packets
    """
    packet = {
        'version': int(bin_str[:3], base=2),
        'type': int(bin_str[3:6], base=2),
    }

    ind = 6
    if packet['type'] == 4:  # literal value
        done = False
        value_str = ''
        while not done:
            next_bits = bin_str[ind:ind+5]
            value_str += next_bits[1:]
            ind += 5
            if next_bits[0] == '0':
                done = True
        packet['value'] = int(value_str, base=2)
        packet['remainder'] = bin_str[ind:]
        return [packet]

    # if not literal, then operator
    len_typ = bin_str[ind]
    ind += 1
    if len_typ == '0':
        length = int(bin_str[ind:ind+15], base=2)
        ind += 15
        remainder = bin_str[ind:]
        sub_packets = []
        num_read = 0
        while num_read < length:
            sub_packets += parse(remainder, process=process)
            num_read += len(remainder) - len(sub_packets[-1]['remainder'])
            remainder = sub_packets[-1]['remainder']
    else:
        num_sub = int(bin_str[ind:ind+11], base=2)
        ind += 11
        remainder = bin_str[ind:]
        sub_packets = []
        for _ in range(num_sub):
            sub_packets += parse(remainder, process=process)
            remainder = sub_packets[-1]['remainder']
    packet['remainder'] = remainder

    if not process:
        return [packet] + sub_packets

    func_types = {
        0: sum,
        1: np.prod,
        2: np.min,
        3: np.max,
    }
    cmp_types = {
        5: operator.gt,
        6: operator.lt,
        7: operator.eq,
    }
    if packet['type'] in func_types:
        packet['value'] = func_types[packet['type']]([packet['value'] for packet in sub_packets])
    else:
        packet['value'] = cmp_types[packet['type']](sub_packets[0]['value'], sub_packets[1]['value'])
    return [packet]


def test16a():
    day16a('D2FE28')
    day16a('38006F45291200')
    day16a('EE00D40C823060')
    assert 16 == day16a('8A004A801A8002F478')
    assert 12 == day16a('620080001611562C8802118E34')
    assert 23 == day16a('C0015000016115A2E0802F182340')
    assert 31 == day16a('A0016C880162017C3686B18A3D4780')


def day16b(input_str):
    """Return the value of the packet, processing all operator packets."""
    if Path(input_str).is_file():
        with open(input_str) as file_obj:
            input_str = file_obj.readline().strip()
    vals = [int(char, base=16) for char in input_str]
    bin_str = ''.join(format(val, '04b') for val in vals)
    return parse(bin_str, process=True)[0]['value']


def test16b():
    assert 3 == day16b('C200B40A82')
    assert 54 == day16b('04005AC33890')
    assert 7 == day16b('880086C3E88112')
    assert 9 == day16b('CE00C43D881120')
    assert 1 == day16b('D8005AC2A8F0')
    assert 0 == day16b('F600BC2D8F')
    assert 0 == day16b('9C005AC2F8F0')
    assert 1 == day16b('9C0141080250320F1802104A08')


if __name__ == '__main__':
    test16a()
    print('Day 16a:', day16a('day16_input.txt'))
    test16b()
    print('Day 16b:', day16b('day16_input.txt'))
