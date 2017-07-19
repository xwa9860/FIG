from comp import Comp
from mat import SS316
from infu import SSU


class Vessel(Comp):

    def __init__(self, temp):
        name = 'VESSEL'
        ss = SSU(temp)
        Comp.__init__(self, temp, name, [SS316(temp)], fill=ss)
