from comp import Comp
from mat import Flibe
from infu import FlibeU

class Downcomer(Comp):

    def __init__(self, temp):
        name = 'Downcomer'
        flibeu = FlibeU(temp)
        Comp.__init__(self, temp, name, [Flibe(temp)], fill=flibeu)
