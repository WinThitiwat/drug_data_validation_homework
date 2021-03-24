from enum import Enum
class DrugClass(Enum):
    '''
    Drug panel classification list
    '''
    NEGATIVE = 'G-Neg'
    POSITIVE = 'G-Pos'
    READMETA = 'read meta'