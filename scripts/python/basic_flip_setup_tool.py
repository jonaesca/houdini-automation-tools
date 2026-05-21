def create_flip_setup():
    """
    FLIP Quick Setup Tool
    Automatically creates a base FLIP fluid simulation setup in Houdini.
    Usage: run from Python Shell or as a Shelf Tool.
    Author: Jonathan Escalera — Houdini Automation Tools
    """
    
    import hou

    #Context reference
    obj = hou.node("/obj")

    #Create geo container
    container = obj.createNode("geo", "flip_sim")

    #Create nodes inside container
    geoinput = container.createNode("null", "replace_with_your_geo")
    points = container.createNode("pointsfromvolume", "create_points")
    points.parm("jitterscale").set(10)
    points.parm("particlesep").setExpression('ch("../dopnet/flip_object/particlesep")')
    dopnet = container.createNode("dopnet", "dopnet")

    #Connect nodes
    points.setInput(0, geoinput)
    dopnet.setInput(0, points)

    #Nodes Visibility
    dopnet.setDisplayFlag(True)
    geoinput.setRenderFlag(False)

    #Move to good pos
    container.layoutChildren()

    #Create nodes in dopnet
    fobject = dopnet.createNode("flipobject", "flip_object")
    fobject.parm("surfacetype").set(1)
    fobject.parm("soppath").set("`opinputpath('..', 0)`")
    fobject.parm("visprim").set(3)
    fobject.parm("closedends").set(True)
    
    fsolver = dopnet.createNode("flipsolver", "flip_solver")
    fsolver.parmTuple("limit_size").set((5, 5, 5))
    gravity = dopnet.createNode("gravity", "gravity")

    #Connect dopnet nodes
    fsolver.setInput(0, fobject)
    gravity.setInput(0, fsolver)

    #Find existing dopnet
    output_node = dopnet.node("output")

    #Connect gravity to dopnet
    output_node.setInput(0, gravity)

    #Dopnet move to good pos
    dopnet.layoutChildren()