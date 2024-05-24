# This will be the box class that will contain the template for the box class
class Box:
    # This will be the constructor of the class Box
    # It will receive the coordinate tensor in the xywh format
    def __init__(self, coordinateTensor):
        # Now we will call the extract information from the tensor method here and get all the information
        self.x1,self.y1,self.x2,self.y2,self.width,self.height,self.topLeft,self.bottomRight,self.topRight,self.bottomLeft = Box.extractBoxesInformationFromCoordinateTensor(coordinateTensor)


    # This will be the method that will check the overlapping between the two boxes
    def checkOverlapping(self, box):
        if (self.x2 < box.x1 or box.x2 < self.x1):
            return False
        if (self.y2 < box.y1 or box.y2 < self.y1):
            return False
    
        return True
    
    def calculateOverlapRatio(self,box):
        # Calculate the (x, y)-coordinates of the intersection rectangle
        inter_x1 = max(self.x1, box.x1)
        inter_y1 = max(self.y1, box.y1)
        inter_x2 = min(self.x2, box.x2)
        inter_y2 = min(self.y2, box.y2)

        # Compute the area of the intersection rectangle
        inter_width = max(0, inter_x2 - inter_x1)
        inter_height = max(0, inter_y2 - inter_y1)
        inter_area = inter_width * inter_height

        # Compute the area of both the prediction and ground-truth rectangles
        box1_area = (self.x2 - self.x1) * (self.y2 - self.y1)
        box2_area = (box.x2 - box.x1) * (box.y2 - box.y1)

        # Compute the area of the union
        smaller_area = min(box1_area,box2_area)

        overlap_ratio = inter_area / float(smaller_area)

        return overlap_ratio

    
    # This will be used to extract the x,y,width,height for the box from the coordinateTensor
    def extractBoxesInformationFromCoordinateTensor(coordinateTensor):
        # This will be the top left x,y, and also the width and the height of the box
        x1,y1,width,height = coordinateTensor

        # This will be the x2,y2 of the box
        x2 = x1 + width
        y2 = y1 + height

        # These will be the set of the x,y coordinates of the box
        topLeft = (x1,y1)
        bottomRight = (x2,y2)
        topRight = (x2,y1)
        bottomLeft = (x1,y2)

        # We will return all of these information
        return [x1,y1,x2,y2,width,height,topLeft,bottomRight,topRight,bottomLeft]
    
    # This will be the function that will get the xy coordinates as
    def getXyCoordinates(self):
        return [self.x1,self.y1,self.x2,self.y2]