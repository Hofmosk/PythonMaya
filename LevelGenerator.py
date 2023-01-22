import maya.cmds as mc
import random


def GenerateRoom():

    global sizeX, sizeZ, heightRoom, StepLenght, StepWidth, NumberStep, Nb_Step, Step_L, Step_W, Room_H, s_x, s_z

    sizeX = 20
    s_x = sizeX
    sizeZ = 20
    s_z = sizeZ
    heightRoom = 5
    Room_H = heightRoom
    nameGround = "Ground"
    groundList = [nameGround]
    stepList =[]

    groundpositionX = 0
    groundpositionZ = 0

    StepLenght=0
    Step_L = StepLenght
    StepHeight=0
    StepWidth=0.0
    Step_W = StepWidth
    NumberStep=0
    Nb_Step = NumberStep


    mc.layoutDialog(ui =ParametersPrompt)

    i = 0

    for ix in range(sizeX):
        for iz in range(sizeZ):
            height_ground = round(random.uniform(0.10, 0.30),2)
            Ground = mc.polyCube(name= nameGround, height = height_ground)
            mc.select(Ground[0])
            mc.move((groundpositionX+(ix-1)),height_ground*0.5,(groundpositionZ+(iz-1)))
            i = i+1
            groundList.append(nameGround+str(i))
            

    groundList.pop(sizeZ*sizeX)
    mc.polyUnite(groundList, name="FinalGround", constructionHistory = False)
    mc.select("FinalGround")
    mc.move(1.5,0,1.5)
    mc.duplicate("FinalGround")
    mc.move(1.5,heightRoom,1.5)


    i = 0

    for i in range(2):        
        WallWest = mc.polyCube(name="WallW1", height = heightRoom, depth= 0.3, width= sizeX)
        mc.xform(translation=[sizeX*0.5,heightRoom*0.5,sizeZ*i])

        WallEast = mc.polyCube(name="WallE1", height = heightRoom, depth= sizeZ, width= 0.3)
        mc.xform(translation=[sizeX*i,heightRoom*0.5,sizeZ*0.5])

    i = 0

    StepHeight = heightRoom / NumberStep
    for i in range(NumberStep):
        Step = mc.polyCube(name="Step1",height=StepHeight, depth = StepLenght, width = StepWidth)
        mc.xform(translation=[StepWidth*i,StepHeight*i,0])
        stepList.append("Step"+str(i+1))
    
    mc.polyUnite(stepList,name="StairCase", constructionHistory = False)
    mc.select("StairCase")
    randomX = round(random.uniform(StepWidth+1,sizeX-(StepWidth*NumberStep)),2)
    randomZ = random.randint(StepLenght,sizeZ-StepLenght)
    mc.move(randomX, StepHeight, randomZ)

    ToBooleen = mc.polyCube(name ="Booleen",height=StepHeight*NumberStep, depth=StepLenght , width= StepWidth*NumberStep)
    mc.select("Booleen")
    mc.xform(piv=[(StepWidth*NumberStep)*-0.5, (StepHeight*NumberStep)*-0.5, 0 ])
    mc.xform(translation=[(randomX+((StepWidth*NumberStep)*0.5)-StepWidth*0.5), ((StepHeight*NumberStep)*0.5)+1, randomZ])

    mc.polyBoolOp('FinalGround1', 'Booleen', op=3, n="Ceiling")
    
def SetParameters(count):
    global NumberStep
    global Nb_Step 
    global StepLenght
    global Step_L
    global StepWidth
    global Step_W
    global heightRoom
    global Room_H
    global sizeX
    global s_x
    global sizeZ
    global s_z

    NumberStep = mc.intField(Nb_Step, query = True, value = True)
    StepLenght = mc.intField(Step_L, query = True, value = True)
    StepWidth = mc.floatField(Step_W, query = True, value = True)
    heightRoom = mc.intField(Room_H, query = True, value = True)
    sizeX = mc.intField(s_x, query = True, value = True)
    sizeZ = mc.intField(s_z, query = True, value = True)

    mc.layoutDialog(dismiss = "OK")

def ParametersPrompt():
    global Nb_Step 
    global Step_L
    global Step_W
    global Room_H
    global s_x
    global s_z

    form = mc.setParent(query = True)
    mc.formLayout(form, width = 400)
    column = mc.columnLayout(adjustableColumn = True)

    mc.rowLayout(numberOfColumns = 2, ad2=2, parent = column)
    s_xT = mc.text(label = "X tile number: ")
    s_x = mc.intField()

    mc.rowLayout(numberOfColumns = 2, ad2=2, parent = column)
    s_zT = mc.text(label = "Z tile number: ")
    s_z = mc.intField()

    mc.rowLayout(numberOfColumns = 2, ad2=2, parent = column)
    Room_HT = mc.text(label = "Room Height: ")
    Room_H = mc.intField()

    mc.rowLayout(numberOfColumns = 2, ad2=2, parent = column)
    Nb_StepT = mc.text(label = "Number Step: ")
    Nb_Step = mc.intField()

    mc.rowLayout(numberOfColumns = 2, ad2=2, parent = column)
    Step_LT = mc.text(label = "Step lenght: ")
    Step_L = mc.intField()

    mc.rowLayout(numberOfColumns = 2, ad2=2, parent = column)
    Step_WT = mc.text(label = "Step width: ")
    Step_W = mc.floatField()

    mc.rowLayout(numberOfColumns = 1, ad2=2, parent = column)
    OkButton = mc.button(label='OK', command= SetParameters )
    spacing = 5

    mc.formLayout(form, edit = True,
                 attachForm =[(column, 'top', spacing),(column, 'left', spacing),(column, 'right', spacing)],
                 attachNone =[(OkButton, "button")])

answer = mc.confirmDialog(title = "Confirm Level", message="This will generate a Room", button=["Create New" , "No"])

if answer == "Create New" :
    GenerateRoom()
