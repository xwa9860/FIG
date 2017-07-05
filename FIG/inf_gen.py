from serp_concept import Cell
from serp_concept import Universe
from serp_concept import Surface
from gen import Gen


class InfGen(Gen):

  def __init__(self):
    self.univ = Universe()

  def parse(self, a_inf, type):
    surf = Surface()
    cell = Cell()
    if type == 's':
      str_list = []
      str_list.append(
          '\n%%--%s\n' %a_inf.name +
          'surf %d inf\n' %surf.id +
          'cell %d %d %s -%d\n' %
          (cell.id, self.univ.id, a_inf.mat_list[0].name, surf.id))
      return ''.join(str_list)
