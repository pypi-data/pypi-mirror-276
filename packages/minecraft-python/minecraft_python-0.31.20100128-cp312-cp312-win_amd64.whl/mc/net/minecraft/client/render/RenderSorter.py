class RenderSorter:

    def __init__(self, player):
        self.__player = player

    def compare(self, c0, c1):
        z3 = c0.isInFrustum
        z4 = c1.isInFrustum
        if z3 and not z4:
            return 1
        elif (not z4 or z3) and c0.distanceToEntitySquared(self.__player) < c1.distanceToEntitySquared(self.__player):
            return 1
        else:
            return -1
