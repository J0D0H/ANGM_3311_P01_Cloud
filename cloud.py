import maya.cmds as cmds
import random
import math

def generate_cloud(base_size=1.5):
    if cmds.objExists("cloud_grp"):
        cmds.delete("cloud_grp")

    cloud_grp = cmds.group(empty=True, name="cloud_grp")
    spheres = []

    for i in range(50):
        radius = random.uniform(base_size * 1, base_size * 1.5)
        sphere = cmds.polySphere(name=f"cloudSphere_{i+1}", r=radius)[0]

        if i == 0:
            pos = (0, 3, 0)
        else:
            pSphere = random.choice(spheres[:max(1, len(spheres)//2)])
            px, py, pz = pSphere["pos"]
            pr = pSphere["radius"]

            theta = random.uniform(0, 2 * math.pi)
            phi = random.uniform(0, math.pi)

            dx = math.sin(phi) * math.cos(theta)
            dy = abs(math.cos(phi))  
            dz = math.sin(phi) * math.sin(theta)

            distance = (pr + radius) * 0.55

            pos = (
                px + dx * distance,
                py + dy * distance,
                pz + dz * distance
            )

        cmds.move(pos[0], pos[1], pos[2], sphere)
        cmds.parent(sphere, cloud_grp)

        spheres.append({
            "name": sphere,
            "radius": radius,
            "pos": pos
        })

generate_cloud()


def create_lightning(start=(0,0,0), end=(0,20,0), segments=20, displacement=1.5):

    if cmds.objExists("lightning_bolt"):
        cmds.delete("lightning_bolt")

    lightning_bolt = cmds.curve(d=1, p=[start, end], name="lightning_bolt")

    cmds.rebuildCurve(lightning_bolt, s=segments, d=1, ch=False, rpo=True)

    cvs = cmds.ls(lightning_bolt + ".cv[*]", fl=True)

    for i in range(1, len(cvs) - 1):

        cmds.move(
            random.uniform(-displacement, displacement),
            random.uniform(-displacement, displacement),
            random.uniform(-displacement, displacement),
            cvs[i],
            r=True
        )

    cmds.select(clear=True)

    return lightning_bolt


create_lightning(start=(0,0,0), end=(0,30,0), segments=25, displacement=2.0)