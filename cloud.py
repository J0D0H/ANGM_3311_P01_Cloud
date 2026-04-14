import maya.cmds as cmds
import random
import math
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore

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

def generate_rain(count=None, size=0.05, area=10):

    if cmds.objExists("rain_grp"):
        cmds.delete("rain_grp")

    rain_grp = cmds.group(empty=True, name="rain_grp")

    if count is None:
        count = random.randint(200, 500)

    for i in range(count):

        sphere = cmds.polySphere(r=size, name=f"rain_{i}")[0]

        x = random.uniform(-area, area)
        y = random.uniform(0, area * 2)
        z = random.uniform(-area, area)

        cmds.move(x, y, z, sphere)

        cmds.parent(sphere, rain_grp)

    return rain_grp

generate_rain()

def get_maya_window():
    ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(ptr), QtWidgets.QWidget)


class WeatherUI(QtWidgets.QDialog):

    def __init__(self, parent=get_maya_window()):
        super(WeatherUI, self).__init__(parent)

        self.setWindowTitle("Weather Tool")
        self.setMinimumWidth(250)

        layout = QtWidgets.QVBoxLayout()

        self.cloud_btn = QtWidgets.QPushButton("Generate Cloud")
        self.lightning_btn = QtWidgets.QPushButton("Generate Lightning")
        self.rain_btn = QtWidgets.QPushButton("Generate Rain")

        layout.addWidget(self.cloud_btn)
        layout.addWidget(self.lightning_btn)
        layout.addWidget(self.rain_btn)

        self.setLayout(layout)

        self.cloud_btn.clicked.connect(generate_cloud)
        self.lightning_btn.clicked.connect(create_lightning)
        self.rain_btn.clicked.connect(generate_rain)


ui = None

def show_ui():
    global ui
    try:
        ui.close()
    except:
        pass

    ui = WeatherUI()
    ui.show()


show_ui()