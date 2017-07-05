
'''
create a universe of infinite flibe
(different from flibe 'material')
'''
from mat import Flibe
from comp import Comp
from flibe_gen import FlibeGen

class FlibeU(Comp):

  def __init__(self, temp, name='Graphite'):
    self.mat = [Graphite(temp)]
    Comp.__init__(self, temp, name, self.mat, GrGen())

  def generate_output(self):
    return self.gen.parse(self, 's')
