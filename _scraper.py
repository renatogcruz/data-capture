"""
Capture the Rhino viewports to an image file. Places the images in a folder with 
the same name as the GH file and in the same directory as the GH file. It 
captures the data used during the optimization process in a CSV file named and 
saved in the same way as described for the images.

    Inputs:
        Toggle:      Activate the component using a boolean toggle
        goalValue:   receives goal value
        width:       width of the screen to be captured
        height:      height of the screen to be captured
        data:        data list    
"""

import scriptcontext as sc
import Rhino as rc
import os
import System

def checkOrMakeFolder():   

    """ Check/makes a "Captures" folder in the GH def folder """

    if ghdoc.Path:
        folder = os.path.dirname(ghdoc.Path)               
        ghDef = ghenv.LocalScope.ghdoc.Name.strip("*") 
        captureFolder = folder + "\\" + str(ghDef)         
        if not os.path.isdir(captureFolder):              
            os.makedirs(captureFolder)                     
        return captureFolder                               


def makeFileName(): 

    """ Make a string with the gh def name + current hourMinuteSecond """

    fileName = str(goalValue)                             
    return fileName                                        

def captureActiveViewToFile(width,height,path): 

	"""
    Captures the active view to an image file at the path. Path looks like this:
    "C:\\Users\\adel\\Desktop\\Captures\\goalValue.png"
    """

    sc.doc = rc.RhinoDoc.ActiveDoc                         
    activeView = sc.doc.Views.ActiveView                   
    imageDim = System.Drawing.Size(width,height)           
    try:                                                   
        imageCap = rc.Display.RhinoView.CaptureToBitmap(activeView,imageDim)
        System.Drawing.Bitmap.Save(imageCap,path)
        rc.RhinoApp.WriteLine(path)
        return path                                        
    except:                                                
        raise Exception(" Capture failed, check the path")


if Toggle:                                                      
    capFolder = checkOrMakeFolder()                             
    fileText = os.path.join(capFolder + ".csv")
    with open(fileText, 'a') as file_object:
        fileName = makeFileName()                               
        count = 0
        try:                                                    
            path = os.path.join(capFolder,fileName + ".png")    
            Path = captureActiveViewToFile(width,height,path)   
        except:                                                
            raise Exception("Capture failed, save the GH definition")
        converte = ', '.join(map(str, data))
        concatenatedData = converte + ", " + fileName + "\n"
        file_object.write(concatenatedData)