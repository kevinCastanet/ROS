from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QApplication, QLabel
from PyQt5 import uic
import sys
import subprocess
import os
import signal


# This is a sample Python script.


class UI_robot(QMainWindow):
    def __init__(self):
        super(UI_robot, self).__init__()
        self.setFixedSize(820, 1000)
        uic.loadUi("ui_robot.ui", self)
        self.etatPatrol = 0
        self.etatNav = 0
        self.etatCamera = 0
        self.navigation = None
        self.camera = None
        self.patrol = None
        self.cameraButton = self.findChild(QPushButton, "cameraButton")
        self.cameraButton.clicked.connect(self.launchCamera)
        self.startNav = self.findChild(QPushButton, "startNav")
        self.startNav.clicked.connect(self.launchNav)
        self.startPatrol = self.findChild(QPushButton, "startPatrol")
        self.startPatrol.clicked.connect(self.launchPat)
        self.Button = self.findChild(QPushButton, "Button")
        self.Button.clicked.connect(self.quitter)
        self.show()

    def launchCamera(self):
        if self.etatCamera == 0:
            print("je lance la camera")
            # subprocess.run("roslaunch cv_basics cv_basics_py.launch", shell=True, check=True)
            self.camera = subprocess.Popen("roslaunch cv_basics cv_basics_py.launch", stdout=subprocess.PIPE,
                                           shell=True, preexec_fn=os.setsid)
            self.cameraButton.setStyleSheet("background-color : green")
            self.etatCamera = 1
        else:
            try:
                self.cameraButton.setStyleSheet("background-color : red")
                os.killpg(os.getpgid(self.camera.pid), signal.SIGTERM)
                self.etatCamera = 0
                # self.startPatrol.kill()
            except:
                pass

    def launchNav(self):
        if self.etatNav == 0:
            print("je lance la map")
            self.startNav.setStyleSheet("background-color : green")
            self.startPatrol.setDisabled(False)
            # subprocess.run("roslaunch cv_basics cv_basics_py.launch", shell=True, check=True)
            self.navigation = subprocess.Popen(
                "roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml",
                stdout=subprocess.PIPE,
                shell=True, preexec_fn=os.setsid)
            self.etatNav = 1
        else:
            try:
                os.killpg(os.getpgid(self.navigation.pid), signal.SIGTERM)
                self.startNav.setStyleSheet("background-color : red")
                # self.startPatrol.kill()
            except:
                pass
            self.etatNav = 0

    def launchPat(self):

        if self.etatPatrol == 0:
            print("je lance la patrouille")
            self.startPatrol.setStyleSheet("background-color : green")
            self.patrol = subprocess.Popen("rosrun project_patrol GoTo.py", stdout=subprocess.PIPE,
                                           shell=True, preexec_fn=os.setsid)
            self.etatPatrol = 1
        else:
            try:
                os.killpg(os.getpgid(self.patrol.pid), signal.SIGTERM)
                # self.startPatrol.kill()
            except:
                pass
            self.etatPatrol = 0

    def quitter(self):
        try:
            os.killpg(os.getpgid(self.navigation.pid), signal.SIGTERM)
            # self.startPatrol.kill()
        except:
            pass
        try:
            os.killpg(os.getpgid(self.camera.pid), signal.SIGTERM)
            # self.startPatrol.kill()
        except:
            pass
        try:
            os.killpg(os.getpgid(self.patrol.pid), signal.SIGTERM)
            # self.startPatrol.kill()
        except:
            pass
        sys.exit()


app = QApplication(sys.argv)
mainWindow = QMainWindow()
uiWindow = UI_robot()

sys.exit(app.exec_())
