from comp import Comp
from mat import Flibe


class Downcomer(Comp):

    def __init__(self, temp):
        name = 'Downcomer'
        Comp.__init__(self, temp, name, [Flibe(temp)])
