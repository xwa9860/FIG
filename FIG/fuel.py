from comp import Comp, Gen
from pbed import FuelUnitCell, PBedLat
from more_itertools import unique_everseen
import mat
import triso
import pb


class Fuel(Comp):

    def __init__(self,
                 fpb_prop,
                 cool_temp,
                 dir_name='serp_input/',
                 name = 'FuelZone',
                 packing_fraction=0.6):
        self.gen_dir_name = dir_name
        fpb_list = self.create_a_pb_unit_cell(fpb_prop, name)
        self.unit_cell = FuelUnitCell(fpb_list,
                                      cool_temp,
                                      packing_fraction=packing_fraction,
                                      dir_name=dir_name)
        self.unit_cell_lat = PBedLat(self.unit_cell,
                                     self.unit_cell.pitch,
                                     dir_name=dir_name)
        Comp.__init__(self, fpb_list[0].temp, name,
                      self.unit_cell_lat.mat_list,
                      gen=Gen(dir_name),
                      fill=self.unit_cell_lat)

    def create_a_pb_unit_cell(self,
                              fpb_prop,
                              uc_name
                              ):
        '''
        fpb_prop: a tuple contains:
            fuel_temps: temperature list for unique pebbles in the unit cell
            a matrix of unique pebbles x n layers of fuel in a triso
            coating_temps: a list that contains temp for each of the non-fuel layers in triso, e.g. 4x5
            cgt: central graphite temperature
            sht: shell temperature
            burnups: a list of 14 burnups
        uc_name: unit cell name
        '''
        fuel_temps, coating_temps, cgt, sht, uc_name, burnups, pb_comp_dir = fpb_prop
        fpb_list = []
        unique_fpb_list = {}
        unique_burnups = list(unique_everseen(burnups))
        unique_burnup_nb = len(unique_burnups)
        assert fuel_temps.shape[0] == unique_burnup_nb, 'wrong dimension %s' %str(fuel_temps.shape)
        assert coating_temps.shape[0] == unique_burnup_nb, 'wrong dimension' 

        # create a list of unique pebbles
        for i, bu in enumerate(unique_burnups):
            pb_name = 'pb%s%d' % (uc_name, bu)
            unique_fpb_list[bu] = self.create_a_fuel_pebble(fuel_temps[bu-1, :], 
                                                            coating_temps[unique_burnups[i]-1, :],
                                                            cgt, sht,
                                                            pb_name,
                                                            unique_burnups[i], 
                                                            pb_comp_dir)
        # create a list of all the 14 fuel pebbles, some of them are exactly the same
        for bu in burnups:
            fpb_list.append(unique_fpb_list[bu])
        return fpb_list

    def create_a_fuel_pebble(self,
                             fuel_temps,
                             coating_temps,
                             cgt, sht,
                             pbname,
                             burnup,
                             pb_comp_dir):
        '''
        create a fuel pebble, assuming all the triso particles in the pebble have the
        same temperature configurations(can have different temp in different triso
        layers though)
        fuel_temps: a list that contains temperature for each fuel
        layer in the triso, 1d array of length 1 or 3
        coating_temps: a list that contains temp for each of the non-fuel layers in triso
        cgt: central graphite temperature
        sht: shell temperature
        burnup: used to choose the fuel mat composition file in pb_comp_dir
        pb_comp_dir: path to the fuel composition in the pebble
        '''
        assert fuel_temps.shape == (1,) or fuel_temps.shape == (3,), 'wrong fuel temp shape:%r' %(fuel_temps.shape)
        assert coating_temps.shape == (1,) or coating_temps.shape == (5,), 'wrong coating temp shape:%r' %(fuel_temps.shape)

        # create fuel materials
        fuels = []
        for i, temp in enumerate(fuel_temps):
            fuel_name = 'fuel%d%s' % (i+1, pbname)
            fuel_input = '%s/fuel_mat%d' % (pb_comp_dir, burnup)
            fuels.append(mat.Fuel(temp, fuel_name, fuel_input))
        # create triso particle
        if coating_temps.shape == (1,):
            tr = triso.Triso(coating_temps,
                             fuels, 
                             dr_config='homogenized',
                             dir_name=self.gen_dir_name)
        else:
            tr = triso.Triso(coating_temps,
                             fuels, 
                             dr_config=None,
                             dir_name=self.gen_dir_name)
        return pb.FPb(tr, cgt, sht, dir_name=self.gen_dir_name)
