from pylogix import PLC
import time
import os

tag_frequency = [
    {'Machine': '1605',
     'nextread': 0,
     'lastcount': 0,
     'frequency': .5,
     'table': 'GFxPRoduction',
     'Count_Tag': 'OP30_4_COUNT.SYSTEM[0].GOOD',
     'Part_Type_Tag': 'ROBOT_R30_4.O.DI37',
     'Part_Type_Map': {'False': '50-5081', 'True': '50-4865'},
     },
    {'Machine': '1606',
     'frequency': .5,
     'nextread': 0,
     'lastcount': 0,
     'table': 'GFxPRoduction',
     'Count_Tag': 'OP30_1_COUNT.SYSTEM[0].GOOD',
     'Part_Type_Tag': 'ROBOT_R30_1.O.DI37',
     'Part_Type_Map': {'False': '50-5081', 'True': '50-4865'},
     },
    {'Machine': '1607',
     'frequency': .5,
     'nextread': 0,
     'lastcount': 0,
     'table': 'GFxPRoduction',
     'Count_Tag': 'OP30_2_COUNT.SYSTEM[0].GOOD',
     'Part_Type_Tag': 'ROBOT_R30_2.O.DI37',
     'Part_Type_Map': {'False': '50-5081', 'True': '50-4865'},
     },
    {'Machine': '1608',
     'frequency': .5,
     'nextread': 0,
     'lastcount': 0,
     'table': 'GFxPRoduction',
     'Count_Tag': 'OP30_3_COUNT.SYSTEM[0].GOOD',
     'Part_Type_Tag': 'ROBOT_R30_3.O.DI37',
     'Part_Type_Map': {'False': '50-5081', 'True': '50-4865'},
     }
]


lastsqltime = ''
sqlfileinterval = 2*60


def loop(taglist, ip, slot=0, minimum_cycle=.5):
    with PLC() as comm:
        comm.IPAddress = ip
        comm.ProcessorSlot = slot

        for entry in taglist:
            # get current timestamp
            now = time.time()
            # make sure we are not polling too fast
            frequency = minimum_cycle if entry['frequency'] < minimum_cycle else entry['frequency']

            if entry['nextread'] < now:
                entry['nextread'] = entry['nextread'] + frequency
                if entry['nextread'] < now:
                    entry['nextread'] = now + frequency
                part_count, part_type = comm.Read(
                    [entry['Count_Tag'], entry['Part_Type_Tag']])
                if part_count.Value > entry['lastcount']:
                    entry['lastcount'] = part_count.Value
                    part_entry(
                        table=entry['table'],
                        timestamp=now,
                        count=part_count.Value,
                        machine=entry['Machine'],
                        parttype=entry['Part_Type_Map'][str(part_type.Value)]
                    )


def part_entry(table, timestamp, count, machine, parttype):
    print('{} made a {} ({})'.format(machine, parttype, count))

    file_path = './sql/{}.sql'.format(str(int(timestamp)))

    with open(file_path, "a+") as file:
        sql = ('INSERT INTO {} '
               '(Machine, Part, PerpetualCount, Timestamp) '
               'VALUES ("{}", "{}" ,{} ,{});\n'.format(
                   table, machine, parttype, count, timestamp))
        file.write(sql)


def get_tags(tags, ip, slot=0):

    with PLC() as comm:
        comm.IPAddress = ip
        comm.ProcessorSlot = slot
        return comm.Read(tags)


if __name__ == "__main__":

    # ret = get_tags(taglist, ip='192.168.1.102')
    # for r in ret:
    #     print(r)

    while True:
        loop(tag_frequency, '192.168.1.102')
