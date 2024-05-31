#!/usr/bin/env python

"""
TODO : implement header info
:copyright: maximilien Lehujeur
"""


class UndeterminedValue(object):
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f'UndeterminedValue("{self.value}")'


def str2float(x: str):
    try:
        return float(x) if len(x.strip()) else None
    except (ValueError, TypeError):
        return UndeterminedValue(x)


def str2int(x: str):
    try:
        return int(x) if len(x.strip()) else None
    except (ValueError, TypeError):
        return UndeterminedValue(x)


def str2str(x: str):
    try:
        x = x.strip()
        return x if len(x) else None
    except (ValueError, TypeError):
        return UndeterminedValue(x)


def determine_revision(header_line: str):
    assert header_line.startswith('H00')

    if "SPS 2.1" in header_line:
        revision = "2.1"

    elif "SPS001" in header_line:
        revision = "0"

    else:
        raise ValueError
    return revision


def determine_file_format(file_name : str):

    if file_name.upper().endswith(".RPS") or file_name.upper().endswith(".SPS"):
        file_format = file_name.split(".")[-1]

    elif file_name.upper().endswith(".XPS"):
        file_format = file_name.split(".")[-1]

    else:
        raise ValueError('unknown file format')

    return file_format


class Record(object):

    def fill(self, line):
        raise NotImplementedError('please use subclasses depending on revision number')


class PointRecord(Record):
    def __init__(self):
        super().__init__()
        self.record_identification = None
        self.line_number = None
        self.point_number = None
        self.point_index = None
        self.point_code = None
        self.static_correction_ms = None
        self.point_depth = None
        self.seismic_datum = None
        self.uphole_time = None
        self.water_depth = None
        self.easting = None
        self.northing = None
        self.elevation = None
        self.day_of_year = None
        self.time_hhmmss = None

    def __str__(self):
        return f"""
    record_identification:{self.record_identification}
    line_number:{self.line_number}
    point_number:{self.point_number}
    point_index:{self.point_index}
    point_code:{self.point_code}
    static_correction_ms:{self.static_correction_ms}
    point_depth:{self.point_depth}
    seismic_datum:{self.seismic_datum}
    uphole_time:{self.uphole_time}
    water_depth:{self.water_depth}
    easting:{self.easting}
    northing:{self.northing}
    elevation:{self.elevation}
    day_of_year:{self.day_of_year}
    time_hhmmss:{self.time_hhmmss}
    """


class PointRecordRev0(PointRecord):
    """S10                   1.01  0   0.0 0   0 0.0 1700768.43198243.3 774.1 0.0000000"""
    def fill(self, line):

        self.record_identification = str2str(line[0])
        self.line_number = str2str(line[1:17])
        self.point_number = str2str(line[17:25])
        self.point_index = str2int(line[25])
        self.point_code = str2str(line[26:28])
        self.static_correction_ms = str2int(line[28:32])
        self.point_depth = str2float(line[33:36])
        self.seismic_datum = str2int(line[36:40])
        self.uphole_time = str2int(line[40:42])
        self.water_depth = str2float(line[42:46])
        self.easting = str2float(line[46:55])
        self.northing = str2float(line[55:65])
        self.elevation = str2float(line[65:71])
        self.day_of_year = str2int(line[71:74])
        self.time_hhmmss = str2str(line[74:80])


class PointRecordRev21(PointRecord):
    "S     10.00    201.00  1       0.0   0     0.01700772.7 3198338.0 766.7 1000000"
    def fill(self, line):

        if len(line[21:23].strip()):
            raise ValueError(f'blank not found, got "{line[21:23]}"')

        self.record_identification = str2str(line[0])
        self.line_number = str2float(line[1:11])
        self.point_number = str2float(line[11:21])
        self.point_index = str2int(line[23])
        self.point_code = str2str(line[24:26])
        self.static_correction_ms = str2int(line[26:30])
        self.point_depth = str2float(line[30:34])
        self.seismic_datum = str2int(line[34:38])
        self.uphole_time = str2int(line[38:40])
        self.water_depth = str2float(line[40:46])
        self.easting = str2float(line[46:55])
        self.northing = str2float(line[55:65])
        self.elevation = str2float(line[65:71])
        self.day_of_year = str2int(line[71:74])
        self.time_hhmmss = str2str(line[74:80])


class RelationRecord(Record):
    def __init__(self):
        super().__init__()
        self.record_identification = None
        self.field_tape_number = None
        self.field_record_number = None
        self.field_record_increment = None
        self.instrument_code = None
        self.source_line_number = None
        self.source_point_number = None
        self.source_point_index = None
        self.from_channel = None
        self.to_channel = None
        self.channel_increment = None
        self.receiver_line_number = None
        self.from_receiver = None
        self.to_receiver = None
        self.receiver_index = None

    def __str__(self):
        return f"""
    record_identification={self.record_identification}
    field_tape_number={self.field_tape_number}
    field_record_number={self.field_record_number}
    field_record_increment={self.field_record_increment}
    instrument_code={self.instrument_code}
    source_line_number={self.source_line_number}
    source_point_number={self.source_point_number}
    source_point_index={self.source_point_index}
    from_channel={self.from_channel}
    to_channel={self.to_channel}
    channel_increment={self.channel_increment}
    receiver_line_number={self.receiver_line_number}
    from_receiver={self.from_receiver}
    to_receiver={self.to_receiver}
    receiver_index={self.receiver_index}    
    """


class RelationRecordRev0(RelationRecord):
    def fill(self, line):
        self.record_identification = str2str(line[0])
        self.field_tape_number = str2str(line[1:7])
        self.field_record_number = str2int(line[7:11])
        self.field_record_increment = str2int(line[11])
        self.instrument_code = str2str(line[12])
        self.source_line_number = str2str(line[13:29])
        self.source_point_number = str2str(line[29:37])
        self.source_point_index = str2int(line[37])
        self.from_channel = str2int(line[38:42])
        self.to_channel = str2int(line[42:46])
        self.channel_increment = str2int(line[46])
        self.receiver_line_number = str2str(line[47:63])
        self.from_receiver = str2str(line[63:71])
        self.to_receiver = str2str(line[71:79])
        self.receiver_index = str2int(line[79])


class RelationRecordRev21(RelationRecord):
    """X0     13271 10                   1.011   597 310                     1     1991"""
    def fill(self, line):
        self.record_identification = str2str(line[0])
        self.field_tape_number = str2str(line[1:7])
        self.field_record_number = str2int(line[7:15])
        self.field_record_increment = str2int(line[15])
        self.instrument_code = str2str(line[16])
        self.source_line_number = str2float(line[17:27])
        self.source_point_number = str2float(line[27:37])
        self.source_point_index = str2int(line[37])
        self.from_channel = str2int(line[38:43])
        self.to_channel = str2int(line[43:48])
        self.channel_increment = str2int(line[48])
        self.receiver_line_number = str2float(line[49:59])
        self.from_receiver = str2float(line[59:69])
        self.to_receiver = str2float(line[69:79])
        self.receiver_index = str2int(line[79])


def read_sps(file_name, verbose: bool = True) -> list:
    # file_format = determine_file_format(file_name)
    record_list = []

    record_object_selector = \
        {"R": {"0": PointRecordRev0, "2.1": PointRecordRev21},
         "S": {"0": PointRecordRev0, "2.1": PointRecordRev21},
         "X": {"0": RelationRecordRev0, "2.1": RelationRecordRev21}}

    revision = None
    with open(file_name, 'r') as fid:
        for line in fid:
            if line[0] == "H":
                if line.startswith('H00'):
                    revision = determine_revision(line)

            elif line[0] in "RSX":
                record: Record
                record = record_object_selector[line[0]][revision]()

                record.fill(line)

                record_list.append(record)
                if verbose:
                    print(record)

    return record_list


def show_records(record_list):
    """only for xps and rps"""
    x, y, i = [], [], []

    for record in record_list:
        x.append(record.easting)
        y.append(record.northing)
        i.append(record.point_number)

    if len(x):
        hdl, = plt.plot(x, y, '+', label=file_name)
        for xx, yy, ii in zip(x, y, i):
            plt.text(xx, yy, ii, color=hdl.get_color())
        return hdl

    return None


if __name__ == '__main__':
    import sys
    import matplotlib.pyplot as plt

    show = "-show" in sys.argv[1:]

    hdl = None
    for file_name in sys.argv[1:]:
        if file_name.startswith('-'):
            continue
        record_list = read_sps(file_name, verbose=True)

    if show and hdl is not None:
        hdl = show_records(record_list)
        plt.legend()
        plt.show()
