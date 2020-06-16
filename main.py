from pylogix import PLC

taglist = [
    'OP30_1_COUNT.SYSTEM[0].GOOD',
    'OP30_2_COUNT.SYSTEM[0].GOOD',
    'OP30_3_COUNT.SYSTEM[0].GOOD',
    'OP30_4_COUNT.SYSTEM[0].GOOD'
]


def get_tags(tags, ip, slot=0):

    with PLC() as comm:
        comm.IPAddress = ip
        comm.ProcessorSlot = slot
        return comm.Read(tags)


if __name__ == "__main__":

    ret = get_tags(taglist, ip='192.168.1.102')
    for r in ret:
        print(r)
