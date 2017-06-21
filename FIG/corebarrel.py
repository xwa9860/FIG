from comp import Comp
from mat import SS316T


class Corebarrel(Comp):

    def __init__(self, temp):
        name = 'Corebarrel'
        Comp.__init__(self, temp, name, [SS316T(temp)])
