import pytest
import ..src


class Mock_Comm():
    def __init__(self, tag_list):
        self.tag_list = tag_list

    def Read(self, tag):
        if tag not in self.tag_list:
            return Response(tag, Status='Connection failure')
        else:
            return Response(tag, Value=self.tag_list[tag])


class Response():
    def __init__(self, tag, Value=None, Status='Success'):
        self.TagName = tag
        self.Value = Value
        self.Status = Status


def get_counter_entry():
    return {
        # type = counter|value
        'type': 'counter',
        # tag is the PLC tag to read
        'tag': 'Program:Production.ProductionData.DailyCounts.DailyTotal',
        # Machine is written into the machine colum on the database
        'Machine': '1617',
        # used internally
        'nextread': 0,
        'lastcount': 0,
        'lastread': 0,
        # how often to try to read the tag in seconds
        'frequency': .5,
        # database table to write to
        'table': 'GFxPRoduction',
        # tag containing what part type is currently running
        'Part_Type_Tag': 'Stn010.PartType',
        # map values in above to a string to write in the part type db colum
        'Part_Type_Map': {'0': '50-4865', '1': '50-5081'}
    }


mock_comm = Mock_Comm(0)


def test_zero_read(mocker):
    mocker.patch('main.part_count_entry')

    counter_entry = get_counter_entry()

    comm = Mock_Comm(
        {counter_entry['tag']: 0, counter_entry['Part_Type_Tag']: 0})

    main.read_counter(counter_entry, comm)

    main.part_count_entry.assert_not_called()
    assert counter_entry['lastcount'] == 0


def test_first_pass_through(mocker):
    mocker.patch('src.part_count_entry')

    counter_entry = get_counter_entry()

    comm = Mock_Comm(
        {counter_entry['tag']: 255, counter_entry['Part_Type_Tag']: 0})

    main.read_counter(counter_entry, comm)

    main.part_count_entry.assert_called_once()
    assert counter_entry['lastcount'] == 255


def test_multiple_entries(mocker):
    mocker.patch('src.part_count_entry')

    counter_entry = get_counter_entry()
    counter_entry['lastcount'] = 250

    comm = Mock_Comm(
        {counter_entry['tag']: 252, counter_entry['Part_Type_Tag']: 0})

    main.read_counter(counter_entry, comm)

    assert main.part_count_entry.call_count == 2
    assert counter_entry['lastcount'] == 252
