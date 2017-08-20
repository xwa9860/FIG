from comp import *
from mat import B4C
from infu import B4CU


class Control_rod(Comp):

    def __init__(self, temp):
        name = 'CRCC_rod'
        B4Cu = B4CU(temp)
        Comp.__init__(self, temp, name, [B4C(temp)], fill=B4Cu)
