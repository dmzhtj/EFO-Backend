from ca import *
from usecase.distribute import Distribute
class Display(Interface):
    dist:Distribute = None
    def run():...