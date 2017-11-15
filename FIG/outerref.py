from comp import Comp
from mat import BGraphite, GraphiteCoolMixT
from infu import BGrU, FlibeGrTU


class OuterRef(Comp):

    def __init__(self, temp):
        name = 'OR'
        gru = BGrU(temp)
        Comp.__init__(self, temp, name, [BGraphite(temp)], fill=gru)


class OuterRef_CoolantChannel(Comp):

    def __init__(self, temp, cool_temp):
        name = 'ORCC'
        mixu = FlibeGrTU(cool_temp)
        Comp.__init__(self, temp, name, [GraphiteCoolMixT(cool_temp)], fill=mixu)
