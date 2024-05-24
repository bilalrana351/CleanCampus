from Box import Box
# This will be the class that will contain the template for the Person class

class Person:
    # This will be the constructor of the class Person
    def __init__(self, trackId, coordinateTensor, className, classId):
        self.id = trackId
        self.box = Box(coordinateTensor)
        self.className = className
        self.classId = classId
        # This will contain information about the litter that the person has in the current state
        self.litters = []


    # This will update the value of the person in accordance with the new value
    def update(self,coordinateTensor):
        self.box = Box(coordinateTensor)

    # This will be the method that will return the trackingIds of all the current litters
    def getTrackingIDsForCurrentLitter(self):
        litterIds = []
        for litter in self.litters:
            litterIds.append(litter.trackId)
        return litterIds
            

    # This will be the function that will check if the person has the specified litter or not, and the result will be then stored in the currentLitter
    # The previous litter will also be updated in a very similar way
    def checkForLitter(self,litters):
        # We want the new litter to start anew
        for litter in litters:
            if (litter.hasPerson == False and self.box.checkOverlapping(litter.box)):
                self.litters.append(litter)
                litter.hasPerson = True
                litter.incomingPersonId = self.id
    
    # These will be the function that will check if the given person has littered or not
    def checkIfHasLittered(self):
        for litter in self.litters:
            if (litter.isOccluded == False):
                print(litter.box.x1,litter.box.x2,litter.box.y1,litter.box.y2)
                print(self.box.x1,self.box.x2,self.box.y1,self.box.y2)
                print(self.box.calculateOverlapRatio(litter.box))
            if (litter.isOccluded == False and (self.box.calculateOverlapRatio(litter.box) < 0.8)):
                return [True,litter.className]
        # In case the person has not done this thing we can safely return False to the output of this function
        return [False,None]