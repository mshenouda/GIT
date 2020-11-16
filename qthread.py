from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import wraps

class UTILITY_GUI_HANDLER(QtCore.QObject):

    signalStatus = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        MainWindow = QtWidgets.QMainWindow()

        # Create a gui object.
        self.gui = Window()
        self.gui.setupUi(MainWindow)

        # Create a new worker thread.
        self.createWorkerThread()

        # Make any cross object connections.
        self._connectSignals()

        MainWindow.show()
        sys.exit(app.exec_())

    def _connectSignals(self):
        self.gui.pushButton2.clicked.connect(self.forceWorkerReset)
        self.signalStatus.connect(self.gui.updateStatus)
        self.parent().aboutToQuit.connect(self.forceWorkerQuit)


    def createWorkerThread(self):

        # Setup the worker object and the worker_thread.
        self.worker = Utility_tab()
        self.worker_thread = QtCore.QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

        # Connect any worker signals
        self.worker.signalStatus.connect(self.gui.updateStatus)
        # self.gui.pushButton.clicked.connect(self.worker.startWork)
        self.gui.pushButton.clicked.connect(self.worker.myWork)


    def forceWorkerReset(self):
        if self.worker_thread.isRunning():
            print('Terminating thread.')
            self.worker_thread.terminate()

            print('Waiting for thread termination.')
            self.worker_thread.wait()

            self.signalStatus.emit('Idle.')

            print('building new working object.')
            self.createWorkerThread()


    def forceWorkerQuit(self):
        if self.worker_thread.isRunning():
            self.worker_thread.terminate()
            self.worker_thread.wait()


class Utility_tab(QtCore.QObject):

    signalStatus = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    @QtCore.pyqtSlot()
    def startWork(self):
        for ii in range(7):
            number = random.randint(0,5000**ii)
            self.signalStatus.emit('Iteration: {}, Factoring: {}'.format(ii, number))
            factors = self.primeFactors(number)
            print('Number: ', number, 'Factors: ', factors)
        self.signalStatus.emit('Idle.')

    def primeFactors(self, n):
        i = 2
        factors = []
        while i * i <= n:
            if n % i:
                i += 1
            else:
                n //= i
                factors.append(i)
        if n > 1:
            factors.append(n)
        return factors

    def a_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """A wrapper function"""

            # Extend some capabilities of func
            return func.__name__
        return wrapper

    @QtCore.pyqtSlot()
    def myWork(self):
        self.signalStatus.emit('This solution')
        while True:
            print('I\'m here')

class Window(QMainWindow):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 100, 150, 80))
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(30, 50, 300, 200))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Address = QtWidgets.QLabel(self.widget)
        self.Address.setObjectName("Address")
        self.horizontalLayout_2.addWidget(self.Address)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Age = QtWidgets.QLabel(self.widget)
        self.Age.setObjectName("Age")
        self.horizontalLayout_3.addWidget(self.Age)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pb_run")
        self.verticalLayout_2.addWidget(self.pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.pushButton2 = QtWidgets.QPushButton(self.widget)
        self.pushButton2.setObjectName("pb_cancel")
        self.verticalLayout_2.addWidget(self.pushButton2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Output"))
        self.Address.setText(_translate("MainWindow", "Address"))
        self.Age.setText(_translate("MainWindow", "Age"))
        self.pushButton.setText(_translate("MainWindow", "Run"))
        self.pushButton2.setText(_translate("MainWindow", "Cancel"))

    @QtCore.pyqtSlot(str)
    def updateStatus(self, status):
        # self.label.setText(self.lineEdit.text()+' '+self.lineEdit_2.text())
        self.label.setText(status)


    # def __init__(self):
    #     QWidget.__init__(self)
    #     self.button_start = QtWidgets.QPushButton('Start', self)
    #     self.button_cancel = QtWidgets.QPushButton('Cancel', self)
    #     self.label_status = QtWidgets.QLabel('', self)
    #
    #     layout = QtWidgets.QVBoxLayout(self)
    #     layout.addWidget(self.button_start)
    #     layout.addWidget(self.button_cancel)
    #     layout.addWidget(self.label_status)
    #
    #     self.setFixedSize(400, 200)
    #
    # @QtCore.pyqtSlot(str)
    # def updateStatus(self, status):
    #     self.label_status.setText(status)


if __name__=='__main__':
    app = QApplication(sys.argv)
    example = UTILITY_GUI_HANDLER(app)
