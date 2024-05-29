class EntitySorter:

    def __init__(self, player):
        self.__player = player

    def compare(self, c0, c1):
        return -1 if c0.distanceToEntitySquared(self.__player) < c1.distanceToEntitySquared(self.__player) else 1
