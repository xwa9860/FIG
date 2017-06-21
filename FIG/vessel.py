from comp import Comp
from mat import SS316T


class Vessel(Comp):

    def __init__(self, temp):
        name = 'VESSEL'
        Comp.__init__(self, temp, name, [SS316T(temp)])
