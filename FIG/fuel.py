from comp import Comp, Gen
from pbed import FuelUnitCell, PBedLat

class Fuel(Comp):

    def __init__(self, fpb_list, cool_temp, dir_name='serp_input/'):
        name = 'ActFuelZone'
        self.unit_cell = FuelUnitCell(fpb_list, cool_temp,
                                      packing_fraction=0.6,
                                      dir_name=dir_name)
        self.unit_cell_lat = PBedLat(self.unit_cell,
                                     self.unit_cell.pitch,
                                     dir_name=dir_name)
        Comp.__init__(self, fpb_list[0].temp, name,
                      self.unit_cell_lat.mat_list,
                      gen=Gen(dir_name),
                      fill=self.unit_cell_lat)


class Fuel_wall(Comp):

    def __init__(self, fpb_list, cool_temp, dir_name='serp_input/'):
        name = 'WallFuelZone'
        self.unit_cell = FuelUnitCell(fpb_list, cool_temp,
                                      packing_fraction=0.6,
                                      dir_name=dir_name)
        self.unit_cell_lat = PBedLat(self.unit_cell,
                                     self.unit_cell.pitch,
                                     dir_name=dir_name)
        Comp.__init__(self, fpb_list[0].temp, name,
                      self.unit_cell_lat.mat_list,
                      gen=Gen(dir_name),
                      fill=self.unit_cell_lat)


class Fuel_act(Comp):

    def __init__(self, fpb_list, cool_temp, dir_name='serp_input/'):
        name = 'ActFuelZone'
        self.unit_cell = FuelUnitCell(fpb_list, cool_temp,
                                      packing_fraction=0.6,
                                      dir_name=dir_name)
        self.unit_cell_lat = PBedLat(self.unit_cell,
                                     self.unit_cell.pitch,
                                     dir_name=dir_name)
        Comp.__init__(self, fpb_list[0].temp, name,
                      self.unit_cell_lat.mat_list,
                      gen=Gen(dir_name),
                      fill=self.unit_cell_lat)


