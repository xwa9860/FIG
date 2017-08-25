from comp import Comp
from crcc_seg_gen import CRCCSegGen


class CRCCSegU(Comp):

  def __init__(self, name='crcc_seg'):
    Comp.__init__(self, 0, name, [], gen=CRCCSegGen())

