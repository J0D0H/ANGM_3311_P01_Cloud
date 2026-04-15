import maya.cmds as cmds
import random
import math
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore

def generate_cloud(count=50, base_size=1.5, spread=1.0):

    if cmds.objExists("cloud_grp"):
        cmds.delete("cloud_grp")

    cloud_grp = cmds.group(empty=True, name="cloud_grp")
    spheres = []

    for i in range(count):
        radius = random.uniform(base_size * 1, base_size * 1.5)
        sphere = cmds.polySphere(name=f"cloudSphere_{i+1}", r=radius)[0]

        if i == 0:
            pos = (0, 18, 0)
        else:
            pSphere = random.choice(spheres[:max(1, len(spheres)//2)])
            px, py, pz = pSphere["pos"]
            pr = pSphere["radius"]

            theta = random.uniform(0, 2 * math.pi)
            phi = random.uniform(0, math.pi)

            dx = math.sin(phi) * math.cos(theta)
            dy = abs(math.cos(phi))
            dz = math.sin(phi) * math.sin(theta)

            distance = (pr + radius) * 0.55 * spread

            pos = (
                px + dx * distance,
                py + dy * distance,
                pz + dz * distance
            )

        cmds.move(pos[0], pos[1], pos[2], sphere)
        cmds.parent(sphere, cloud_grp)

        spheres.append({"pos": pos, "radius": radius})

    return cloud_grp

def create_lightning(amount=1, displacement=1.5):

    if cmds.objExists("lightning_grp"):
        cmds.delete("lightning_grp")

    lightning_grp = cmds.group(empty=True, name="lightning_grp")

    for b in range(amount):

        start = (random.uniform(-1, 1), 20, random.uniform(-1, 1))
        end = (random.uniform(-3, 3), 0, random.uniform(-3, 3))

        bolt = cmds.curve(d=1, p=[start, end], name=f"lightning_{b}")
        cmds.rebuildCurve(bolt, s=20, d=1, ch=False, rpo=True)

        cvs = cmds.ls(bolt + ".cv[*]", fl=True)

        for i in range(1, len(cvs) - 1):
            cmds.move(
                random.uniform(-displacement, displacement),
                random.uniform(-displacement, displacement),
                random.uniform(-displacement, displacement),
                cvs[i],
                r=True
            )

        cmds.parent(bolt, lightning_grp)

    return lightning_grp

def generate_rain(count=300, size=0.05, area=10):

    if cmds.objExists("rain_grp"):
        cmds.delete("rain_grp")

    rain_grp = cmds.group(empty=True, name="rain_grp")

    for i in range(count):
        sphere = cmds.polySphere(r=size, name=f"rain_{i}")[0]

        x = random.uniform(-area, area)
        y = random.uniform(0, area * 2)
        z = random.uniform(-area, area)

        cmds.move(x, y, z, sphere)
        cmds.parent(sphere, rain_grp)

    return rain_grp

def get_maya_window():
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QWidget)

class WeatherUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        if parent is None:
            parent = get_maya_window()

        super(WeatherUI, self).__init__(parent)

        self.setWindowTitle("Weather Tool")
        self.setMinimumWidth(320)

        layout = QtWidgets.QVBoxLayout()

        #Cloud
        cloud_row = QtWidgets.QHBoxLayout()
        self.cloud_toggle = QtWidgets.QCheckBox("Cloud")
        self.cloud_toggle.setChecked(False)

        cloud_row.addWidget(self.cloud_toggle)

        layout.addLayout(cloud_row)

        self.cloud_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.cloud_slider.setRange(10, 150)
        self.cloud_slider.setValue(50)
        layout.addWidget(QtWidgets.QLabel("Cloud Density"))
        layout.addWidget(self.cloud_slider)

        self.cloud_size_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.cloud_size_slider.setRange(5, 30)
        self.cloud_size_slider.setValue(10)
        layout.addWidget(QtWidgets.QLabel("Cloud Size / Spread"))
        layout.addWidget(self.cloud_size_slider)


        #Rain
        rain_row = QtWidgets.QHBoxLayout()
        self.rain_toggle = QtWidgets.QCheckBox("Rain")

        rain_row.addWidget(self.rain_toggle)

        layout.addLayout(rain_row)

        self.rain_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rain_slider.setRange(50, 2000)
        self.rain_slider.setValue(300)
        layout.addWidget(QtWidgets.QLabel("Rain Amount"))
        layout.addWidget(self.rain_slider)

        # Lightning
        lightning_row = QtWidgets.QHBoxLayout()
        self.lightning_toggle = QtWidgets.QCheckBox("Lightning")
        
        lightning_row.addWidget(self.lightning_toggle)
        
        layout.addLayout(lightning_row)
        self.lightning_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.lightning_slider.setRange(1, 6)
        self.lightning_slider.setValue(2)
        layout.addWidget(QtWidgets.QLabel("Lightning Amount"))
        layout.addWidget(self.lightning_slider)

        self.setLayout(layout)

        self.cloud_toggle.stateChanged.connect(self.update_cloud)
        self.lightning_toggle.stateChanged.connect(self.update_lightning)
        self.rain_toggle.stateChanged.connect(self.update_rain)

        self.cloud_slider.valueChanged.connect(self.update_cloud)
        self.cloud_size_slider.valueChanged.connect(self.update_cloud)
        self.rain_slider.valueChanged.connect(self.update_rain)
        self.lightning_slider.valueChanged.connect(self.update_lightning)


        self.update_cloud()
        self.update_rain()
        self.update_lightning()



    def update_cloud(self, *args):
        if self.cloud_toggle.isChecked():
            generate_cloud(
                count=self.cloud_slider.value(),
                base_size=self.cloud_size_slider.value() * 0.1,
                spread=self.cloud_size_slider.value() * 0.1
            )
        else:
            if cmds.objExists("cloud_grp"):
                cmds.delete("cloud_grp")

    def update_rain(self, *args):
        if self.rain_toggle.isChecked():
            generate_rain(count=self.rain_slider.value())
        else:
            if cmds.objExists("rain_grp"):
                cmds.delete("rain_grp")

    def update_lightning(self, *args):
        if self.lightning_toggle.isChecked():
            create_lightning(amount=self.lightning_slider.value())
        else:
            if cmds.objExists("lightning_grp"):
                cmds.delete("lightning_grp")

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
