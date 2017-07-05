from comp import *
from mat import Graphite, Flibe
from infu import GrU, FlibeU

class CenterRef(Comp):

    def __init__(self, temp):
        name = 'CR'
        gru = GrU(temp)
        Comp.__init__(self, temp, name, [Graphite(temp)], fill=gru)


class CenterRef_CoolantChannel(Comp):

    def __init__(self, temp):
        name = 'CRCC'
        flibeu = FlibeU(temp)
        Comp.__init__(self, temp, name, [Flibe(temp)], fill=flibeu)


class CRCC_liner(Comp):

    def __init__(self, temp):
        name = 'CRCC_liner'
        flibeu = FlibeU(temp)
        Comp.__init__(self, temp, name, [Flibe(temp)], fill=flibeu)
