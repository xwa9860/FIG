'''
create a universe of infinite volume of a material
'''
from mat import Graphite, BGraphite, B4C, Flibe, Zr
from mat import SS316, GraphiteCoolMix, ShieldMat
from mat import GraphiteCoolMixT, SiC
from comp import Comp
from inf_gen import InfGen

class InfU(Comp):

  def __init__(self, temp, mat, name='Inf'):
    Comp.__init__(self, temp, name, [mat], gen=InfGen())


class GrU(InfU):

  def __init__(self, temp, name='Graphite'):
    InfU.__init__(self, temp, Graphite(temp), name)

class BGrU(InfU):

  def __init__(self, temp, name='BGraphite'):
    InfU.__init__(self, temp, BGraphite(temp), name)

class FlibeU(InfU):

  def __init__(self, temp, name='Flibe'):
    InfU.__init__(self, temp, Flibe(temp), name)


class FlibeGrU(InfU):

  def __init__(self, temp, name='flibeGrMix'):
    InfU.__init__(self, temp, GraphiteCoolMix(temp), name)


class FlibeGrTU(InfU):

  def __init__(self, temp, name='flibeGrTMix'):
    InfU.__init__(self, temp, GraphiteCoolMixT(temp), name)


class SSU(InfU):

  def __init__(self, temp, name='SS316'):
    InfU.__init__(self, temp, SS316(temp), name)

class ZrU(InfU):

  def __init__(self, temp, name='Zr'):
    InfU.__init__(self, temp, Zr(temp), name)

class B4CU(InfU):

  def __init__(self, temp, name='B4C'):
    InfU.__init__(self, temp, B4C(temp), name)

class SiCU(InfU):

  def __init__(self, temp, name='SiC'):
    InfU.__init__(self, temp, SiC(temp), name)


class ShieldU(InfU):

  def __init__(self, temp, name='Shield'):
    InfU.__init__(self, temp, ShieldMat(temp), name)
