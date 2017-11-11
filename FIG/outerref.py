from comp import Comp
from mat import BGraphite, GraphiteCoolMix
from infu import BGrU, FlibeGrU


class OuterRef(Comp):

    def __init__(self, temp):
        name = 'OR'
        gru = BGrU(temp)
        Comp.__init__(self, temp, name, [BGraphite(temp)], fill=gru)


class OuterRef_CoolantChannel(Comp):

    def __init__(self, temp, cool_temp):
        name = 'ORCC'
        mixu = FlibeGrU(cool_temp)
        Comp.__init__(self, temp, name, [GraphiteCoolMix(cool_temp)], fill=mixu)
