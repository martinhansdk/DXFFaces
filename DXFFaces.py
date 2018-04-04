#Author-Martin Hans
#Description-Export the selected faces to DXF.

import adsk.core, adsk.fusion, adsk.cam, traceback
from . import DXFFacesCommand

commandName1 = 'DXFFaces'
commandDescription1 = 'Better DXF export for Fusion 360'
commandResources1 = './resources'
cmdId1 = 'cmdID_DXFFaces'
myWorkspace1 = 'FusionSolidEnvironment'
myToolbarPanelID1 = 'SolidScriptsAddinsPanel'

debug = False

newCommand1 = DXFFacesCommand.DXFFacesCommand(commandName1, commandDescription1, commandResources1, cmdId1, myWorkspace1, myToolbarPanelID1, debug)



def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        newCommand1.onRun()
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        newCommand1.onStop()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
