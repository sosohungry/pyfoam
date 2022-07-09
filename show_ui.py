import sys

import PyFoam.Basics.Utilities
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from UI.main_windows import Ui_MainWindow
from UI.viscosity import Ui_Form as viscosityFoam
from UI.tension import Ui_Form as tensioForm
from UI.velocity import Ui_Form as velocityFoam
from UI.lubricity import Ui_Form as lubricityFoam
from UI.flow_line import Ui_Form as flowlineFoam
from code.changfile import *

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)
        self.viscosity = Myviscosity()
        self.tension = Mytension()
        self.velocity = Myvelocity()
        self.lubricity = Mylubricity()
        self.flowline = Myflowline()




        self.actionOpen.triggered.connect(self.openFile)

        self.pushButton.clicked.connect(self.viscosityShow)
        self.pushButton_2.clicked.connect(self.tensionShow)
        self.pushButton_3.clicked.connect(self.velocityShow)
        self.pushButton_4.clicked.connect(self.lubricityShow)
        self.pushButton_5.clicked.connect(self.flowlineShow)


        self.viscosity.pushButton.clicked.connect(self.viscosityRun)
        self.tension.pushButton.clicked.connect(self.tensionRun)
        self.velocity.pushButton.clicked.connect(self.velocityRun)
        self.lubricity.pushButton.clicked.connect(self.lubricityRun)
        self.flowline.pushButton.clicked.connect(self.flowlineRun)

    def openFile(self):
        # self.file, ok = QFileDialog.getOpenFileNames(self, "打开", "./example", "ALL Files (*);;openfoam Files (*.foam)")
        self.dir = QFileDialog.getExistingDirectory(self)
        self.statusbar.showMessage(self.dir)


    def viscosityShow(self):
        self.viscosity.show()
        self.viscosityFile = self.dir + "/constant/transportProperties"
        self.viscosity.lineEdit.setText(self.viscosityFile)

        water_nu = ParsedParameterFile(self.viscosityFile)["water"]["nu"]
        oil_nu = ParsedParameterFile(self.viscosityFile)["oil"]["nu"]
        print(water_nu, oil_nu)

        self.viscosity.lineEdit_2.setText(str(water_nu[2]))
        self.viscosity.lineEdit_3.setText(str(oil_nu[2]))


    def tensionShow(self):
        self.tension.show()
        self.tensionFile = self.dir + "/constant/transportProperties"
        simga = ParsedParameterFile(self.tensionFile)["sigma"]
        self.tension.lineEdit.setText(self.tensionFile)
        print(simga)
        self.tension.lineEdit_2.setText(str(simga[2]))

    def velocityShow(self):
        self.velocity.show()
        self.velocityFile = self.dir + "/0/U"
        self.velocity.lineEdit.setText(self.velocityFile)
        boundaryField = ParsedParameterFile(self.velocityFile)
        boundaryName = boundaryField["boundaryField"]
        for i in (boundaryName):
            self.velocity.comboBox.addItem(i)

        default_num = boundaryName.keys()[0]
        print(default_num)
        self.velocity.lineEdit_2.setText(str(boundaryName[default_num]["type"]))
        self.velocity.lineEdit_3.setText(str(boundaryName[default_num]["value"]))


    def lubricityShow(self):
        self.lubricity.show()
        self.lubricityFile = self.dir + "/0/alpha.water"
        self.lubricity.lineEdit.setText(self.lubricityFile)
        boundaryField = ParsedParameterFile(self.lubricityFile)
        boundaryName = boundaryField["boundaryField"]
        for i in (boundaryName):
            self.lubricity.comboBox.addItem(i)

        default_num = boundaryName.keys()[0]
        print(default_num)
        self.lubricity.lineEdit_2.setText(str(boundaryName[default_num]["type"]))
        self.lubricity.lineEdit_3.setText(str(boundaryName[default_num]["value"]))


    def flowlineShow(self):
        self.flowline.show()

        self.flowlineFile = self.dir + "/0/alpha.water"
        self.flowline.lineEdit.setText(self.flowlineFile)
        boundaryField = ParsedParameterFile(self.flowlineFile)
        boundaryName = boundaryField["boundaryField"]
        for i in (boundaryName):
            self.flowline.comboBox.addItem(i)

        default_num = boundaryName.keys()[0]
        print(default_num)
        self.lubricity.lineEdit_2.setText(str(boundaryName[default_num]["type"]))
        self.lubricity.lineEdit_3.setText(str(boundaryName[default_num]["theta0"]))




    def viscosityRun(self):

        source_path = self.dir
        # print(self.viscosity.lineEdit_2.text())
        change_num_water = float(self.viscosity.lineEdit_2.text())
        print(change_num_water)
        change_num_oil = float(self.viscosity.lineEdit_3.text())
        print(change_num_oil)

        did_copy = self.viscosity.checkBox.isChecked()
        print(did_copy)

        changeViscosity(source_path=source_path,
                        change_num_water=change_num_water,
                        change_num_oil=change_num_oil,
                        did_copy=did_copy)
        print("success")


    def tensionRun(self):
        source_path = self.dir
        # print(self.viscosity.lineEdit_2.text())
        change_num = float(self.tension.lineEdit_2.text())
        print(change_num)

        did_copy = self.tension.checkBox.isChecked()
        print(did_copy)

        changeTension(source_path=source_path,
                      change_num=change_num,
                        did_copy=did_copy)
        print("success")


    def velocityRun(self):
        source_path = self.dir
        change_wall = self.velocity.comboBox.currentText()
        change_type = self.velocity.lineEdit_2.text()
        change_num = self.velocity.lineEdit_3.text()
        did_copy = self.velocity.checkBox.isChecked()

        print(change_wall)
        changeVelocity(source_path=source_path,
                       boundaryName=change_wall,
                       change_num=change_num,
                       did_copy=did_copy)
        print("success")


    def lubricityRun(self):
        source_path = self.dir
        change_wall = self.lubricity.comboBox.currentText()
        change_type = self.lubricity.lineEdit_2.text()
        change_num = self.lubricity.lineEdit_3.text()
        did_copy = self.lubricity.checkBox.isChecked()

        print(change_wall)
        changeLubricity(source_path=source_path,
                       boundaryName=change_wall,
                       change_num=change_num,
                       did_copy=did_copy)
        print("success")

    def flowlineRun(self):
        source_path = self.dir
        change_wall = self.flowline.comboBox.currentText()
        change_type = self.flowline.lineEdit_2.text()
        change_num = self.flowline.lineEdit_3.text()
        did_copy = self.flowline.checkBox.isChecked()

        print(change_wall)
        changeContactAngle(source_path=source_path,
                        change_wall=change_wall,
                        change_num=change_num,
                        did_copy=did_copy)
        print("success")



class Myviscosity(QWidget, viscosityFoam):
     def __init__(self):
         super(Myviscosity, self).__init__()
         self.setupUi(self)

class Mytension(QWidget, tensioForm):
    def __init__(self):
        super(Mytension, self).__init__()
        self.setupUi(self)

class Myvelocity(QWidget, velocityFoam):
    def __init__(self):
        super(Myvelocity, self).__init__()
        self.setupUi(self)

class Mylubricity(QWidget, lubricityFoam):
    def __init__(self):
        super(Mylubricity, self).__init__()
        self.setupUi(self)
class Myflowline(QWidget, flowlineFoam):
    def __init__(self):
        super(Myflowline, self).__init__()
        self.setupUi(self)





if __name__=="__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())