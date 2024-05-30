from enum import IntEnum
from .charset import RDSCharsetDecode
from .group import Group, dataclass

@dataclass
class Details:
    details=True
@dataclass
class PSDetails(Details):
    segment: int
    di: int
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
class DecodedGroup:
    raw_group:Group
    pi: int
    tp: bool
    pty: int
    group: int
    details:Details
class GroupDecoder:
    def _decode_0(self, group: Group, dgroup: DecodedGroup):
        segment = group.b & 3
        ta = (group.b >> 4) & 1
        ms = (group.b >> 3) & 1
        if segment == 3:
            di = (group.b >> 2) & 9
        else:
            di = 0
        details = PSDetails(segment,di,bool(ms),bool(ta),"")

        char_1 = (group.d >> 8) & 0xFF
        char_2 = group.d & 0xFF
        details.text += RDSCharsetDecode.translate(char_1)
        details.text += RDSCharsetDecode.translate(char_2)

        dgroup.details = details
        return group, dgroup
    def _decode_2(self, group: Group, dgroup: DecodedGroup):
        dgroup.group = 2
        segment = group.b & 15
        ab = (group.b >> 4) & 1
        details = RTDetails(segment,bool(ab),"")

        if not group.is_version_b:
            char_1 = (group.c >> 8) & 0xFF
            char_2 = group.c & 0xFF
            char_3 = (group.d >> 8) & 0xFF
            char_4 = group.d & 0xFF
            details.text += RDSCharsetDecode.translate(char_1)
            details.text += RDSCharsetDecode.translate(char_2)
            details.text += RDSCharsetDecode.translate(char_3)
            details.text += RDSCharsetDecode.translate(char_4)
        else:
            char_1 = (group.d >> 8) & 0xFF
            char_2 = group.d & 0xFF
            details.text += RDSCharsetDecode.translate(char_1)
            details.text += RDSCharsetDecode.translate(char_2)

        dgroup.details = details
        return group, dgroup
    def _decode_1(self, group:Group, dgroup:DecodedGroup):
        dgroup.group = 1
        tmp = (group.c & 0xFF)
        details = ECCLICDetails(0,False)
        if tmp < 0x46:
            details.is_lic = True
        details.data = tmp
        dgroup.details = details
        return group, dgroup
    def _decode_10(self, group:Group, dgroup:DecodedGroup):
        dgroup.group = 10
        segment = group.b & 3
        ab = (group.b >> 4) & 1
        details = PTYNDetails(segment,bool(ab),"")
        char_1 = (group.c >> 8) & 0xFF
        char_2 = group.c & 0xFF
        char_3 = (group.d >> 8) & 0xFF
        char_4 = group.d & 0xFF
        details.text += RDSCharsetDecode.translate(char_1)
        details.text += RDSCharsetDecode.translate(char_2)
        details.text += RDSCharsetDecode.translate(char_3)
        details.text += RDSCharsetDecode.translate(char_4)
        dgroup.details = details
        return group, dgroup
    def _decode_4(self, group:Group, dgroup:DecodedGroup):
        dgroup.group = 4
        #TODO: add 4A group decoding
        return group, dgroup
    def decode(self, group: Group):
        out = DecodedGroup(group,group.a,False,0,0,None)
        out.pty = ((group.b >> 5) & 31)
        out.tp = bool((group.b >> 10) & 1)
        gr = (group.b >> 12) & ((1 << 12) - 1)
        if group.is_version_b and gr != 0: gr -= 1
        match gr:
            case 0:
                group, out = self._decode_0(group, out)
            case 2:
                group, out = self._decode_2(group, out)
            case 1:
                group, out = self._decode_1(group, out)
            case 10:
                group, out = self._decode_10(group, out)
            case _:
                out.group = gr
        return out