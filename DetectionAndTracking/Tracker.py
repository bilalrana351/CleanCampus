from Person import Person
from Litter import Litter

# This will be the file that will contain the template for the tracker class 
class Tracker:
    # This will be the constructor of the class tracker
    def __init__(self):
        self.persons = []
        self.litters = []
        self.idList = []
    
    # This will be the method that will return the tracking id of all the persons
    def returnTrackingID(self):
        for person in self.persons:
            self.idList.append(person.trackId)

    # This will be the method that will update the tracker after every pass
    def update(self,classes,trackIds,tensors):
        # We will add some logic that will be used to make sure that the boxes that are not in the frame anymore are removed from the frame
        self.removeObjectsNotAnymore(trackIds)

        # We will find out the values for all the classes
        for class_,trackId,tensor in zip(classes,trackIds,tensors):
            if trackId not in self.idList:
                if (class_ == 0):
                    self.persons.append(Person(trackId,tensor,self.getClassNameFromClassID(class_),class_))
                    self.idList.append(trackId)
                else:
                    self.litters.append(Litter(trackId,tensor,self.getClassNameFromClassID(class_),class_))
                    self.idList.append(trackId)
            else:
                self.updateTrackId(trackId,tensor)

        # We will now check out for the conditions in which we would iterate over all the persons and find out the litter that they have in their hand
        # We will also update the states of the person
        for person in self.persons:
            person.checkForLitter(self.litters) 
        
        litterBugInfo = self.detectLitterBug()

        if (litterBugInfo[0] == True):
            personBoundingBox = litterBugInfo[1]
            return [True,litterBugInfo[1],litterBugInfo[2]]
        else:
            return [False,None,None]

    # This will be the method that will return true if a litterbug has been detected, alongwith his/her box coordinates, so that a picture of him her is captured
    def detectLitterBug(self):
        for person in self.persons:
            detectionResult = person.checkIfHasLittered()
            if (detectionResult[0] == True):
                # We will return a list of lower,upper,left,right coordinates from the bounding box
                return [True,person.box.getXyCoordinates(),detectionResult[1]]
        return [False,None,None]  

    # Now this will be the method that will be used to detect whether someone has littered or not, it will return the reference to the person class of that person, and will also give the reference to the type of the litter that the  


    # This will be the function that will get the class name from the classID
    def getClassNameFromClassID(self,classId):
        if (classId == 0):
            return "person"
        elif (classId == 1):
            return "paper"
        elif (classId == 2):
            return "cardboard"
        elif (classId == 3):
            return "can"
        elif (classId == 4):
            return "plastic"
        elif (classId == 5):
            return "cup"
        
    # THis will be the function that will update the track ID based on the specific conditions
    def updateTrackId(self,trackId,newTensor):
        for person in self.persons:
            if trackId == person.id:
                person.update(newTensor)
        for litter in self.litters:
            if trackId == litter.trackId:
                litter.update(newTensor)

    # This will be the function that will check all the persons against the litter at all the conditions
    def allocateLitterToPerson(self):
        for person in self.persons:
            for litter in self.litters:
                if (litter.hasPerson == False):
                    person.checkForLitter(litter)

    # This will remove all the objects that are not in the frame anymore
    def removeObjectsNotAnymore(self,incomingIds):
        for person in self.persons:
            if (person.id not in incomingIds):
                self.persons.remove(person)
                self.idList.remove(person.id)
        
        for litter in self.litters:
            if (litter.trackId not in incomingIds):
                # We will need to have second thoughts on this function
                litter.isOccluded = True