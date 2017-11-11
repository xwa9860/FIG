from comp import Comp
from mat import ShieldMat
from infu import ShieldU


class Shield(Comp):

    def __init__(self, temp):
        name = 'SHIELD'
        ss = ShieldU(temp)
        Comp.__init__(self, temp, name, [ShieldMat(temp)], fill=ss)
