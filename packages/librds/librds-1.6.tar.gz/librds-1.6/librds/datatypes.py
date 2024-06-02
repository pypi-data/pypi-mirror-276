from dataclasses import dataclass
        
@dataclass
class Group:
    """This is a basic group function to store the blocks"""
    a:int
    b:int
    c:int
    d:int
    is_version_b: bool=None #should be none if theres no group set
    def to_list(self):
        return [self.a, self.b, self.c, self.d]
    def __iter__(self):
        return self.to_list()
    def to_bytes(self):
        return [self.a.to_bytes(2,)]

@dataclass
class GroupIdentifier:
    group_number: int
    group_version: bool


@dataclass
class Details:
    details=True

@dataclass
class PSDetails(Details):
    segment: int
    di_stereo:bool
    di_artificial_head:bool
    di_compressed:bool
    di_dpty:bool
    ms: bool
    ta: bool
    text: str

@dataclass
class RTDetails(Details):
    segment: int
    ab: bool
    text: str

@dataclass
class PTYNDetails(Details):
    segment: int
    ab: bool
    text: str

@dataclass
class ECCLICDetails(Details):
    data:int
    is_lic:bool

@dataclass
class CTDetails(Details):
    mjd: int
    hour: int
    minute: int
    time_sense: bool
    local_offset: int

@dataclass
class TDCDetails(Details):
    channel: int
    data: list[int]

@dataclass
class InHouseDetails(Details):
    data: list[int]

@dataclass
class ODAAidDetails(Details):
    oda_group: GroupIdentifier
    aid:int
    scb:int

@dataclass
class DecodedGroup:
    raw_group:Group
    pi: int
    tp: bool
    pty: int
    group: GroupIdentifier
    details:Details