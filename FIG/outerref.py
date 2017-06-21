from comp import Comp
from mat import Graphite, GraphiteCoolMix


class OuterRef(Comp):

    def __init__(self, temp):
        name = 'OR'
        Comp.__init__(self, temp, name, [Graphite(temp)])


class OuterRef_CoolantChannel(Comp):

    def __init__(self, temp, cool_temp):
        name = 'ORCC'
        Comp.__init__(self, temp, name, [GraphiteCoolMix(cool_temp)])
