#!/usr/bin/python
from coolant_gen import CoolantGen
from mat import Flibe
from sets import Set
from comp import Comp


class Coolant(Comp):

    def __init__(self, temp, name = 'Coolant'):
        self.filling = Set([Flibe(temp)])
        Comp.__init__(self, temp, name, self.filling, CoolantGen())

    def generate_output(self):
        return self.gen.parse(self, 's')
