#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL
 
#############################################################################
class Quelclient(QtGui.QWidget):
 
    def __init__(self, parent=None):
        super(Quelclient, self).__init__(parent)
        self.setWindowTitle(u"Quel client")
 
        # créer un lineEdit
        self.lineEdit = QtGui.QLineEdit(self)
        # créer un bouton
        self.bouton = QtGui.QPushButton(u"Ok", self)
        self.bouton.clicked.connect(self.ok_m)
        # positionner les widgets dans la fenêtre
        posit = QtGui.QGridLayout()
        posit.addWidget(self.lineEdit, 0, 0)
        posit.addWidget(self.bouton, 1, 0)
        self.setLayout(posit)
 
    def ok_m(self):
        # emettra un signal "fermeturequelclient()" avec l'argument cité
        self.emit(SIGNAL("fermeturequelclient(PyQt_PyObject)"), unicode(self.lineEdit.text())) 
        # fermer la fenêtre
        self.close()
 
#############################################################################
class Principal(QtGui.QMainWindow):
 
    def __init__(self, parent=None):
        """Initialise la fenêtre"""
        super(Principal, self).__init__(parent)
        self.setWindowTitle(u"Code test")
 
        # mettre un fond (nécessaire avec un QMainWindow)
        self.setCentralWidget(QtGui.QFrame())
        # créer un lineEdit
        self.lineEdit = QtGui.QLineEdit(self.centralWidget())
        # créer un bouton
        self.bouton = QtGui.QPushButton(u"Sélectionnez un client !", self.centralWidget())
        self.bouton.clicked.connect(self.quelclient_m)
        # positionner les widgets sur le fond de la fenêtre
        posit = QtGui.QGridLayout()
        posit.addWidget(self.lineEdit, 0, 0)
        posit.addWidget(self.bouton, 1, 0)
        self.centralWidget().setLayout(posit)
 
    def quelclient_m(self):
        """Lance la deuxième fenêtre"""
        self.quelclient = Quelclient()
        # en cas de signal "fermeturequelclient()" reçu de self.quelclient => exécutera clienchoisi 
        self.connect(self.quelclient, SIGNAL("fermeturequelclient(PyQt_PyObject)"), self.clientchoisi) 
        # la deuxième fenêtre sera 'modale' (la première fenêtre sera inactive)
        self.quelclient.setWindowModality(QtCore.Qt.ApplicationModal)
        # appel de la deuxième fenêtre
        self.quelclient.show()
 
    def clientchoisi(self, x):
        """affiche le résultat x transmis par le signal à l'arrêt de la deuxième fenêtre"""
        self.lineEdit.setText(x)
 
#############################################################################
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('plastique'))
    main = Principal()
    main.show()
    sys.exit(app.exec_())