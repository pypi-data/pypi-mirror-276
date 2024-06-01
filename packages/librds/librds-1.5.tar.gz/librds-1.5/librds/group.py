from dataclasses import dataclass
@dataclass
class Group:
    """This is a basic group function to store the blocks, the get and set items have been added for backwards compatibility"""
    a:int
    b:int
    c:int
    d:int
    is_version_b: bool=None #should be none if theres no group set
    def to_list(self):
        return [self.a, self.b, self.c, self.d]
    def __iter__(self):
        return self.to_list()