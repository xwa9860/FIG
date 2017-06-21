from comp import *
from mat import Graphite, Flibe


class CenterRef(Comp):

    def __init__(self, temp):
        name = 'CR'
        Comp.__init__(self, temp, name, [Graphite(temp)])


class CenterRef_CoolantChannel(Comp):

    def __init__(self, cool_temp):
        name = 'CRCC'
        Comp.__init__(self, cool_temp, name, [Flibe(cool_temp)])


class CRCC_liner(Comp):

    def __init__(self, temp):
        name = 'CRCC_liner'
        Comp.__init__(self, temp, name, [Flibe(temp)])
