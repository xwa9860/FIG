#!/usr/bin/python


class CmpObj(object):

    def __init__(self, temp, name):
        self.temp = temp
        self.name = name

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.temp == other.temp and
                self.name == other.name)

    def __ne__(self, other):
            return not self.__eq__(other)

    def __hash__(self):
        if not isinstance(self.name, str):
            print self.name
            print 'is not string but %s'  %type(self.name)
        else:
            return hash(self.__class__.__name__+self.name + str(self.temp))
