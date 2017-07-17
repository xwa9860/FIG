#!/usr/bin/python
from coolant_gen import CoolantGen
from mat import Flibe
from comp import Comp


class Coolant(Comp):

    def __init__(self, temp, name = 'Coolant'):
        self.mat = [Flibe(temp)]
        Comp.__init__(self, temp, name, self.mat, CoolantGen())

    def generate_output(self):        return self.gen.parse(self, 's')
