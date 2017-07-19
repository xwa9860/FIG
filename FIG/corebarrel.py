from comp import Comp
from mat import SS316
from infu import SSU


class Corebarrel(Comp):

    def __init__(self, temp):
        name = 'Corebarrel'
        ssu = SSU(temp)
        Comp.__init__(self, temp, name, [SS316(temp)], fill=ssu)
