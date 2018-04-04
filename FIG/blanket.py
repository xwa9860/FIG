from comp import Comp
from comp import Gen
from pbed import GraphiteUnitCell, PBedLat


class Blanket(Comp):

    def __init__(self, pb_temp, cool_temp,
                 packing_fraction=0.6,
                 dir_name='serp_input/'):
        self.pb_temp = pb_temp
        self.cool_temp = cool_temp
        name = 'Blanket'
        self.unit_cell = GraphiteUnitCell(self.pb_temp, self.cool_temp,
                                          packing_fraction=packing_fraction,
                                          dir_name=dir_name)
        self.unit_cell_lat = PBedLat(self.unit_cell, self.unit_cell.pitch)
        Comp.__init__(self, pb_temp, name, self.unit_cell_lat.mat_list,
                      gen=Gen(dir_name),
                      fill=self.unit_cell_lat)
