import maya.cmds as cmds
import random

def generate_cloud():
    # delete old cloud
    if cmds.objExists("cloud_grp"):
        cmds.delete("cloud_grp")

    cloud_grp = cmds.group(empty=True, name="cloud_grp")

    for i in range(15):  # fixed number for now
        sphere = cmds.polySphere(name=f"cloud_{i+1}")[0]

        x = random.uniform(-5, 5)
        y = random.uniform(0, 3)
        z = random.uniform(-5, 5)

        cmds.move(x, y, z, sphere)
        cmds.parent(sphere, cloud_grp)

generate_cloud()