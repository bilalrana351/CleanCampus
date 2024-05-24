from Box import Box

# This will be the class containing the information about the litter
class Litter:
    def __init__(self,trackId,coordinateTensor,className,classId):
        self.box = Box(coordinateTensor)
        self.className = className
        self.classId = classId
        self.trackId = trackId
        self.hasPerson = False
        self.incomingPersonId = -1
        self.isOccluded = False

    # This will update the value of the person in accordance with the new value
    def update(self,coordinateTensor):
        self.box = Box(coordinateTensor)