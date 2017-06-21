#!/usr/bin/python
from control_rod_gen import ControlRodGen
from comp import Comp
from mat import Flibe, B4C
from sets import Set


class ControlRod(Comp):
    '''
    8 control rods channels in the center reflector
    in this program, it's either fully inserted or retracted out of the core and
    the channels is filled with coolant
    '''
    def __init__(self, temp, inserted=None):
        if inserted==None:
            mat = Flibe(temp)
        else:
            mat = B4C(temp)
        self.temp = temp
        self.filling = Set([mat])
        Comp.__init__(self, temp, 'controlRod', self.filling, ControlRodGen)
