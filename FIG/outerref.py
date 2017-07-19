from comp import Comp
from mat import Graphite, GraphiteCoolMix
from infu import GrU, FlibeGrU


class OuterRef(Comp):

    def __init__(self, temp):
        name = 'OR'
        gru = GrU(temp)
        Comp.__init__(self, temp, name, [Graphite(temp)], fill=gru)


class OuterRef_CoolantChannel(Comp):

    def __init__(self, temp, cool_temp):
        name = 'ORCC'
        mixu = FlibeGrU(cool_temp)
        Comp.__init__(self, temp, name, [GraphiteCoolMix(cool_temp)], fill=mixu)
