class GroupInterface:
    def getPS(text: str):
        if len(text) > 8: text = text[:8]
        return text.ljust(8), 4
    def getRT(text: str,full:bool=False):
        if len(text) >= 64: text = text[:64]
        elif not full: text += "\r" # http://www.interactive-radio-system.com/docs/EN50067_RDS_Standard.pdf page 26
        if not full:
            while len(text) % 4: # if we don't have text to equally spread across 4 charcter parts then we add padding
                text = text + " "
            segments = 0
            for _ in range(len(text)):
                segments = segments + 0.25 # 1/4 = 0.25 | 0.25*4 = 1
            if not float(segments).is_integer(): raise Exception("Segment error (segment is not int)")
            if int(segments) > 16: return None, None
            return text, int(segments)
        else:
            return text.ljust(64), 16
    def getPTYN(text: str):
        if len(text) > 8: text = text[:8]
        return text.ljust(8), 2