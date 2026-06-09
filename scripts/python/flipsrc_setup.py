"""
flip_src_setup.py
teo_nemac · Sac-Actun FX Pipeline

Creates a standardized FLIP simulation setup in Houdini.
Includes SOP-level sourcing, attribute noise, velocity wrangle,
and a DOP network with solver, gravity, and static collider.

Author : Jonathan Escalera
Role   : Technical Artist · Founder
Studio : teonemac
Version: 1.1.0 · 2026
"""

import hou


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CONTAINER_NAME = "flip_sim"
PARTICLE_SEP   = 0.05
LIMIT_SIZE     = (5, 5, 5)

VEX_SPEED_NOISE = """v@v = set(1, 0, 0);
v@v += curlnoise(v@P*5+@Time)*ch('noise_mult');
"""


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

def _get_user_settings():
    """Prompt user to override default constants via UI dialog."""

    result = hou.ui.readMultiInput(
        "teo_nemac · Sac-Actun FLIP Setup",
        input_labels=(
            "Container Name",
            "Particle Separation",
            "Limit Size X",
            "Limit Size Y",
            "Limit Size Z",
        ),
        initial_contents=(
            CONTAINER_NAME,
            str(PARTICLE_SEP),
            str(LIMIT_SIZE[0]),
            str(LIMIT_SIZE[1]),
            str(LIMIT_SIZE[2]),
        ),
        buttons=("Create", "Cancel"),
    )

    # 0 = Create, 1 = Cancel
    if result[0] == 1:
        return None

    values = result[1]
    return {
        "container_name" : values[0],
        "particle_sep"   : float(values[1]),
        "limit_size"     : (float(values[2]), float(values[3]), float(values[4])),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def create_flip_src_setup():

    # --- Get user settings ---
    settings = _get_user_settings()
    if settings is None:
        return  # user cancelled — exit cleanly

    obj = hou.node("/obj")

    # Create geo container
    container = obj.createNode("geo", settings["container_name"])

    # Create SOP Nodes
    geosrc   = container.createNode("null", "insert_your_src_here")
    var      = container.createNode("attribnoise::2.0")
    var.parm("attribs").set("P")
    var.parm("displace").set(True)
    var.parm("fractal").set(3)
    var.parm("noiserange").set(1)
    var.parm("animated").set(True)
    flipsrc  = container.createNode("flipsource", "flip_source")
    flipsrc.parm("jitterseed").setExpression('$FF')
    wrangle  = container.createNode("attribwrangle", "speed_noise")
    wrangle.parm("snippet").set(VEX_SPEED_NOISE)
    dopnet   = container.createNode("dopnet", "flip_sim")
    coll     = container.createNode("null", "insert_your_coll_here")

    # SOP Connect Nodes
    var.setInput(0, geosrc)
    flipsrc.setInput(0, var)
    wrangle.setInput(0, flipsrc)
    dopnet.setInput(0, wrangle)
    dopnet.setInput(3, coll)

    # SOP Nodes Visibility
    coll.setRenderFlag(0)
    geosrc.setRenderFlag(0)
    dopnet.setDisplayFlag(1)
    dopnet.setRenderFlag(1)

    # SOP Move to Good Pos
    container.layoutChildren()

    # Create DOP Nodes
    flipobject = dopnet.createNode("flipobject", "flip_object")
    flipobject.parm("closedends").set(True)
    flipobject.parm("surfacetype").set(1)
    flipobject.parm("soppath").set("`opinputpath('..', 0)`")
    flipobject.parm("visprim").set(3)
    flipobject.parm("particlesep").set(settings["particle_sep"])
    volsrc     = dopnet.createNode("volumesource", "volume_source")
    volsrc.parm("input").set(1)
    flipsolver = dopnet.createNode("flipsolver", "flip_solver")
    flipsolver.parmTuple("limit_size").set(settings["limit_size"])
    grav       = dopnet.createNode("gravity", "gravity")
    merge      = dopnet.createNode("merge", "merge")
    merge.parm("affectortype").set(2)
    staticobj  = dopnet.createNode("staticobject", "bring_your_coll_geo_here")
    staticobj.parm("soppath").set("`opinputpath('..', 3)`")

    # DOP Connect Nodes
    flipsolver.setInput(0, flipobject)
    flipsolver.setInput(3, volsrc)
    grav.setInput(0,       flipsolver)
    merge.setInput(0,      grav)
    merge.setInput(1,      staticobj)

    # Find Existing Output and Connect
    output_node = dopnet.node("output")
    output_node.setInput(0, merge)

    # Move to Good Pos
    dopnet.layoutChildren()

    # Network Box
    netbox = container.createNetworkBox()
    netbox.setComment("teo_nemac · Sac-Actun FLIP Setup · v1.1")
    netbox.addItem(geosrc)
    netbox.addItem(var)
    netbox.addItem(flipsrc)
    netbox.addItem(wrangle)
    netbox.addItem(coll)
    netbox.addItem(dopnet)
    netbox.fitAroundContents()

    hou.ui.displayMessage(
        "FLIP setup ready.",
        title="teo_nemac · Sac-Actun FX Pipeline"
    )


create_flip_src_setup()