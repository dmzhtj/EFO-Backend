from usecase.usecase import UseCase
from random import random
class RandDistribute(UseCase.Distribute):
    def score(self,article,thumbnail):
        return random() * 2 - 1