from enum import Enum, IntEnum

def get_from_list(input:list,index:int,default=None):
    """This is a simple function to remove index errors from the group generators"""
    try:
        return input[index]
    except IndexError:
        return default

def calculate_mjd(year: int, month: int, day:int):
    """Year: e.x 2024
    Month: (starts from 0) 0 - Jan, 1 - Feb ...
    Day - (starts from 1)"""
    l = 1 if (month == 0 or month == 1) else 0
    return (
        14956 + day + 
        int(
            ((year - 1900) - l) * 365.25
        ) +
        int(
            (month + 2 + l * 12) * 30.6001
        )
    )

def calculate_ymd(mjd:int):
    """Returns the same format as calculate_mjd, so you can encode and decode without any conversions"""
    jd = mjd + 2_400_001
    ljd = jd + 68569
    
    njd = int((4 * ljd / 146097))
    ljd = ljd - int(((146097 * njd + 3) / 4))
    
    year = int((4000 * (ljd + 1) / 1461001))
    ljd = ljd - int(((1461 * year / 4))) + 31
    
    month = int((80 * ljd / 2447))
    
    day = ljd - int((2447 * month / 80))
    
    ljd = int((month / 11));
    month = int((month + 2 - 12 * ljd))
    year = int((100 * (njd - 49) + year + ljd))
    return year, (month-1), day

class Groups(Enum):
    PS = 0
    PS_B = 1
    RT = 2
    RT_B = 3
    PTYN = 4
    ECC = 5
    LIC = 6
    TDA = 7
    TDA_B = 8
    IN_HOUSE = 9
    IN_HOUSE_B = 10

class GroupSequencer:
    """you can use this code to sequence though anything"""
    def __init__(self, sequence:list[IntEnum]) -> None:
        self.cur_idx = 1
        self.sequence = sequence
    def get_next(self):
        if len(self.sequence) == 0: return
        if self.cur_idx > len(self.sequence): self.cur_idx = 1
        prev = self.sequence[self.cur_idx-1]
        self.cur_idx += 1
        return prev
    def change_sequence(self, sequence:list[IntEnum]):
       self.sequence = sequence
       self.cur_idx = 1
    def __len__(self):
        return len(self.sequence)
    def __iter__(self):
        return self.sequence
