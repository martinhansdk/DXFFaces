import adsk.core, adsk.fusion, traceback
from .dxfwrite import DXFEngine as dxf
from . import Fusion360CommandBase

def printFace(face):
    out=open(r"C:\Users\marti\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\DXFFaces\output.txt", "w")
    print("printFace(%s)" % face, file=out)

    drawing = dxf.drawing(r"C:\Users\marti\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\DXFFaces\test.dxf")
    drawing.add_layer('LINES')


    for coEdge in face.loops[0].coEdges:
        print("coEdge(%s): %s" % (coEdge.classType, coEdge), file=out)
        points=[]
        for cp in coEdge.geometry.controlPoints:
            print("  %s" % str(cp.asArray()), file=out)
            points.append(tuple(cp.asArray()))


        drawing.add(dxf.line(points[0], points[1], color=7, layer='LINES'))



    drawing.save()



# Utility casts various inputs into appropriate Fusion 360 Objects
def getSelectedObjects(selectionInput):
    objects = []
    for i in range(0, selectionInput.selectionCount):
        selection = selectionInput.selection(i)
        selectedObj = selection.entity
        if adsk.fusion.BRepBody.cast(selectedObj) or \
           adsk.fusion.BRepFace.cast(selectedObj) or \
           adsk.fusion.Occurrence.cast(selectedObj):
           objects.append(selectedObj)
    return objects

# Utility to get and format the various inputs
def getInputs(command, inputs):
    selectionInput = None

    for inputI in inputs:
        global commandId
        if inputI.id == command.parentCommandDefinition.id + '_selection':
            selectionInput = inputI
        elif inputI.id == command.parentCommandDefinition.id + '_spacing':
            spacingInput = inputI
            spacing = spacingInput.value

    objects = getSelectedObjects(selectionInput)

    if not objects or len(objects) == 0:
        # TODO this probably requires much better error handling
        return
    # return(objects, plane, edge, spacing, subAssy)

    return (objects, spacing)


class DXFFacesCommand(Fusion360CommandBase.Fusion360CommandBase):
    def onPreview(self, command, inputs):
        pass
    def onDestroy(self, command, inputs, reason_):
        pass
    def onInputChanged(self, command, inputs, changedInput):
        pass
    def onExecute(self, command, inputs):

        # Get Input values
        # (objects, plane, edge, spacing, subAssy) = getInputs(command, inputs)
        (faces, spacing) = getInputs(command, inputs)

        # Apply Joints
        for face in faces:
            printFace(face)

        # Arrange Components
        #arrangeComponents(newFaces, plane, edge, spacing)

    def onCreate(self, command, inputs):

        selectionInput = inputs.addSelectionInput(command.parentCommandDefinition.id + '_selection', 'Select other faces', 'Select bodies or occurrences')
        selectionInput.setSelectionLimits(1,0)
        selectionInput.addSelectionFilter('PlanarFaces')

        app = adsk.core.Application.get()
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        unitsMgr = design.unitsManager
        spacingInput = inputs.addValueInput(command.parentCommandDefinition.id + '_spacing', 'Component Spacing',
                                            unitsMgr.defaultLengthUnits,
                                                adsk.core.ValueInput.createByReal(2.54))
        # createSubAssyInput = inputs.addBoolValueInput(command.parentCommandDefinition.id + '_subAssy', "Create Sub-Assembly", True)
