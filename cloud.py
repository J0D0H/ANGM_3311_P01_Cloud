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