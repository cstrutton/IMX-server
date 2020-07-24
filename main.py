from pylogix import PLC
import time
import os


tag_frequency_op30 = [
    {
        'type': 'counter',
        'tag': 'OP30_4_COUNT.SYSTEM[0].GOOD',
        'Machine': '1605',
        'nextread': 0,
        'lastcount': 0,
        'frequency': .5,
        'table': 'GFxPRoduction',
        'Part_Type_Tag': 'ROBOT_R30_4.O.DI37',
        'Part_Type_Map': {'False': '50-5081', 'True': '50-4865'},
    },
    {
        'type': 'counter',
        'tag': 'OP30_1_COUNT.SYSTEM[0].GOOD',
        'Machine': '1606',
        'frequency': .5,
        'nextread': 0,
        'lastcount': 0,
        'table': 'GFxPRoduction',
        'Part_Type_Tag': 'ROBOT_R30_1.O.DI37',
        'Part_Type_Map': {'False': '50-5081', 'True': '50-4865'},
    },
    {
        'type': 'counter',
        'tag': 'OP30_2_COUNT.SYSTEM[0].GOOD',
        'Machine': '1607',
        'frequency': .5,
        'nextread': 0,
        'lastcount': 0,
        'table': 'GFxPRoduction',
        'Part_Type_Tag': 'ROBOT_R30_2.O.DI37',
        'Part_Type_Map': {'False': '50-5081', 'True': '50-4865'},
    },
    {
        'type': 'counter',
        'tag': 'OP30_3_COUNT.SYSTEM[0].GOOD',
        'Machine': '1608',
        'frequency': .5,
        'nextread': 0,
        'lastcount': 0,
        'table': 'GFxPRoduction',
        'Part_Type_Tag': 'ROBOT_R30_3.O.DI37',
        'Part_Type_Map': {'False': '50-5081', 'True': '50-4865'},
    }
]


def loop(taglist, ip, slot=0, minimum_cycle=.5):
    with PLC() as comm:
        comm.IPAddress = ip
        comm.ProcessorSlot = slot

        for entry in taglist:

            # get current timestamp
            now = time.time()

            frequency = entry['frequency']

            # make sure we are not polling too fast
            if frequency < minimum_cycle:
                frequency = minimum_cycle

            # handle first pass through
            if entry['nextread'] == 0:
                entry['nextread'] = now

            if entry['nextread'] > now:
                continue  # too soon move on

            if entry['type'] == 'counter':
                # print('Read Counter:', entry['tag'])
                entry['lastread'] = now
                read_counter(entry, comm)
                # set the next read timestamp
                entry['nextread'] += frequency

            if entry['type'] == 'value':
                # print('Read Value:', entry['tag'])
                entry['lastread'] = now
                read_value(entry, comm)
                # set the next read timestamp
                entry['nextread'] += frequency


def read_value(value_entry, comm):
    print(time.time(), ':', comm.Read(entry['tag']))


def read_counter(counter_entry, comm):
    # read the tag
    part_count = comm.Read(counter_entry['tag'])
    if part_count.Status != 'Success':
        print('failed to read ', part_count)
        return

    part_type = comm.Read(counter_entry['Part_Type_Tag'])
    if part_type.Status != 'Success':
        return

    if (part_count.Value == 0) or (part_count.Value > counter_entry['lastcount']):
        # save this reading
        counter_entry['lastcount'] = part_count.Value
        # post this reading

        part_count_entry(
            table=counter_entry['table'],
            timestamp=counter_entry['lastread'],
            count=part_count.Value,
            machine=counter_entry['Machine'],
            parttype=counter_entry['Part_Type_Map'][str(part_type.Value)]
        )


def part_count_entry(table, timestamp, count, machine, parttype):
    print('{} made a {} ({})'.format(machine, parttype, count))

    file_path = '/var/local/SQL/{}.sql'.format(
        str(int(timestamp)))

    with open(file_path, "a+") as file:
        sql = ('INSERT INTO {} '
               '(Machine, Part, PerpetualCount, Timestamp) '
               'VALUES ("{}", "{}" ,{} ,{});\n'.format(
                   table, machine, parttype, count, timestamp))
        file.write(sql)


if __name__ == "__main__":

    while True:
        loop(tag_frequency, ip='192.168.1.2', slot=3, minimum_cycle=.5)
