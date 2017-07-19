'''
create a universe of infinite volume of a material
'''
from mat import Graphite, Flibe, SS316, GraphiteCoolMix
from comp import Comp
from inf_gen import InfGen

class InfU(Comp):

  def __init__(self, temp, mat, name='Inf'):
    Comp.__init__(self, temp, name, [mat], gen=InfGen())


class GrU(InfU):

  def __init__(self, temp, name='Graphite'):
    InfU.__init__(self, temp, Graphite(temp), name)


class FlibeU(InfU):

  def __init__(self, temp, name='Flibe'):
    InfU.__init__(self, temp, Flibe(temp), name)


class FlibeGrU(InfU):

  def __init__(self, temp, name='flibeGrMix'):
    InfU.__init__(self, temp, GraphiteCoolMix(temp), name)


class SSU(InfU):

  def __init__(self, temp, name='SS316'):
    InfU.__init__(self, temp, SS316(temp), name)
