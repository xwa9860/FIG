from comp import Comp
from mat import Graphite, GraphiteCoolMix
from gru import GraphiteU


class OuterRef(Comp):

    def __init__(self, temp):
        name = 'OR'
        gru = GraphiteU(temp)
        Comp.__init__(self, temp, name, [Graphite(temp)], fill=gru)


class OuterRef_CoolantChannel(Comp):

    def __init__(self, temp, cool_temp):
        name = 'ORCC'
        Comp.__init__(self, temp, name, [GraphiteCoolMix(cool_temp)])
