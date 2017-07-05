'''
create a universe of infinite volume of a material
'''
from mat import Graphite, Flibe
from comp import Comp
from inf_gen import InfGen

class InfU(Comp):

  def __init__(self, temp, mat, name='Inf'):
    Comp.__init__(self, temp, name, [mat], InfGen())

  def generate_output(self):
    return self.gen.parse(self, 's')


class GrU(InfU):

  def __init__(self, temp, name='Graphite'):
    InfU.__init__(self, temp, Graphite(temp), name)


class FlibeU(InfU):

  def __init__(self, temp, name='Flibe'):
    InfU.__init__(self, temp, Flibe(temp), name)
