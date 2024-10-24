class Comparison:
    def compTreasure(treasure1, treasure2):
        priority1 = -(treasure1.arrival_time + treasure1.size)
        priority2 = -(treasure2.arrival_time + treasure2.size)
        if priority1 != priority2:
            return priority1 > priority2
        else:
            return treasure1.id < treasure2.id
    def compCrewmate(Crewmate1,Crewmate2):
        if Crewmate1.load<Crewmate2.load:
            return True
        else:
            return False