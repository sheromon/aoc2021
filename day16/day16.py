from pathlib import Path


def day16a(input_str):
    if Path(input_str).is_file():
        with open(input_str) as file_obj:
            input_str = file_obj.readline().strip()
    vals = [int(char, base=16) for char in input_str]
    bin_str = ''.join(format(val, '04b') for val in vals)
    packets = parse(bin_str)
    val = sum(packet['ver'] for packet in packets)
    return val


def parse(bin_str):
    packet = {
        'ver': int(bin_str[:3], base=2),
        'typ': int(bin_str[3:6], base=2),
    }

    ind = 6
    if packet['typ'] == 4:  # literal value
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
        packet['last_ind'] = ind
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
            sub_packets += parse(remainder)
            num_read += len(remainder) - len(sub_packets[-1]['remainder'])
            remainder = sub_packets[-1]['remainder']
        return [packet] + sub_packets
    else:
        num_sub = int(bin_str[ind:ind+11], base=2)
        ind += 11
        remainder = bin_str[ind:]
        sub_packets = []
        for _ in range(num_sub):
            sub_packets += parse(remainder)
            remainder = sub_packets[-1]['remainder']
        return [packet] + sub_packets


def test16a():
    day16a('D2FE28')
    day16a('38006F45291200')
    day16a('EE00D40C823060')
    assert 16 == day16a('8A004A801A8002F478')
    assert 12 == day16a('620080001611562C8802118E34')
    assert 23 == day16a('C0015000016115A2E0802F182340')
    assert 31 == day16a('A0016C880162017C3686B18A3D4780')


def day16b(input_path):
    pass


def test16b():
    assert 3 == day16b('C200B40A82')


if __name__ == '__main__':
    test16a()
    print('Day 16a:', day16a('day16_input.txt'))
    # test16b()
    # print('Day 16b:', day16b('day16_input.txt'))
