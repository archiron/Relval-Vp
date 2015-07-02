#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

import os,sys,subprocess

from getEnv import env
from fonctions import cmd_test, liste, cmd_folder_creation, get_collection_list, get_choix_calcul, clean_files, copy_files
		
class ovalGui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('DQMGui v0.0.9')

        self.cmsenv = env()
        self.texte = self.cmsenv.cmsAll()
        self.choix_calcul = 'Full'   # default
        self.choix_job = '8nh'       # default
        self.choix_etape = 'analyze' # default
		
		# creation du grpe Etapes
        self.QGBox0 = QGroupBox("Etapes")
        self.QGBox0.setMaximumHeight(150)
        self.QGBox0.setMaximumWidth(100)
        self.radio01 = QRadioButton("analyze") # Liste par defaut
        self.radio02 = QRadioButton("finalize")
        self.radio03 = QRadioButton("store")
        self.radio04 = QRadioButton("publish")
        self.radio01.setChecked(True)
        self.connect(self.radio01, SIGNAL("clicked()"), self.radio01Clicked) 
        self.connect(self.radio02, SIGNAL("clicked()"), self.radio02Clicked) 
        self.connect(self.radio03, SIGNAL("clicked()"), self.radio03Clicked) 
        self.connect(self.radio04, SIGNAL("clicked()"), self.radio04Clicked)
        vbox0 = QVBoxLayout()
        vbox0.addWidget(self.radio01)
        vbox0.addWidget(self.radio02)
        vbox0.addWidget(self.radio03)
        vbox0.addWidget(self.radio04)
        vbox0.addStretch(1)
        self.QGBox0.setLayout(vbox0)
				
		# creation du grpe Calcul
        self.QGBox1 = QGroupBox("Calcul")
        self.QGBox1.setMaximumHeight(150)
        self.QGBox1.setMaximumWidth(100)
        self.radio11 = QRadioButton("FULL") # par defaut
        self.radio12 = QRadioButton("PU")
        self.radio13 = QRadioButton("FAST")
        self.radio11.setChecked(True)
        self.connect(self.radio11, SIGNAL("clicked()"), self.radio11Clicked) 
        self.connect(self.radio12, SIGNAL("clicked()"), self.radio12Clicked) 
        self.connect(self.radio13, SIGNAL("clicked()"), self.radio13Clicked) 
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.radio11)
        vbox1.addWidget(self.radio12)
        vbox1.addWidget(self.radio13)
        vbox1.addStretch(1)
        self.QGBox1.setLayout(vbox1)
        
		# creation du grpe store/force
        self.QGBox2 = QGroupBox("store/force")
        self.QGBox2.setMaximumHeight(150)
        self.QGBox2.setMinimumHeight(150)
        self.QGBox2.setMaximumWidth(100)		
        self.radio21 = QRadioButton("store") # par defaut
        self.radio22 = QRadioButton("force")
        self.radio21.setChecked(True)
        self.connect(self.radio21, SIGNAL("clicked()"), self.radio21Clicked)
        self.connect(self.radio22, SIGNAL("clicked()"), self.radio22Clicked)
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.radio21)
        vbox2.addWidget(self.radio22)
        vbox2.addStretch(1)
        self.QGBox2.setLayout(vbox2)
        self.QGBox2.setEnabled(False)
        self.QGBox2.setVisible(False)
				
		# creation du grpe liste des collections
        self.QGBox31 = QGroupBox("Collections")
        self.QGBox32 = QGroupBox("Collections")
        self.QGBox31.setMaximumHeight(150)
        self.QGBox32.setMaximumHeight(150)
        self.QGBox31.setMinimumHeight(150)
        self.QGBox32.setMinimumHeight(150)
        self.QGBox31.setVisible(True)
        self.QGBox32.setVisible(False)
        self.check31 = QCheckBox("Pt10Startup_UP15")
        self.check32 = QCheckBox("Pt35Startup_UP15")
        self.check33 = QCheckBox("Pt1000Startup_UP15")
        self.check34 = QCheckBox("QcdPt80Pt120Startup_13")
        self.check35 = QCheckBox("TTbarStartup_13")
        self.check36 = QCheckBox("ZEEStartup_13")
        self.check37 = QCheckBox("TTbarStartup_13")
        self.check38 = QCheckBox("ZEEStartup_13")
        self.check31.setChecked(True)
        self.check32.setChecked(True)
        self.check33.setChecked(True)
        self.check34.setChecked(True)
        self.check35.setChecked(True)
        self.check36.setChecked(True)
        self.check37.setChecked(True)
        self.check38.setChecked(True)
        vbox31 = QVBoxLayout()
        vbox32 = QVBoxLayout()
        vbox31.addWidget(self.check31)
        vbox31.addWidget(self.check32)
        vbox31.addWidget(self.check33)
        vbox31.addWidget(self.check34)
        vbox31.addWidget(self.check35)
        vbox31.addWidget(self.check36)
        vbox32.addWidget(self.check37)
        vbox32.addWidget(self.check38)
        vbox31.addStretch(1)
        vbox32.addStretch(1)
        self.QGBox31.setLayout(vbox31)
        self.QGBox32.setLayout(vbox32)
        
		# creation du grpe store/force
        self.QGBox4 = QGroupBox("batch/interactif")
        self.QGBox4.setMaximumHeight(150)
        self.QGBox4.setMinimumHeight(150)
        self.QGBox4.setMaximumWidth(100)		
        self.radio41 = QRadioButton("batch") # par defaut
        self.radio42 = QRadioButton("interactif")
        self.radio41.setChecked(True)
        self.connect(self.radio41, SIGNAL("clicked()"), self.radio41Clicked)
        self.connect(self.radio42, SIGNAL("clicked()"), self.radio42Clicked)
        vbox4 = QVBoxLayout()
        vbox4.addWidget(self.radio41)
        vbox4.addWidget(self.radio42)
        vbox4.addStretch(1)
        self.QGBox4.setLayout(vbox4)
        
		# creation du grpe choix job
        self.QGBox5 = QGroupBox("Choix job")
        self.QGBox5.setMaximumHeight(150)
        self.QGBox5.setMinimumHeight(150)
        self.QGBox5.setMaximumWidth(100)		
        self.radio51 = QRadioButton("8nh") # par defaut
        self.radio52 = QRadioButton("1nh")
        self.radio51.setChecked(True)
        self.connect(self.radio51, SIGNAL("clicked()"), self.radio51Clicked)
        self.connect(self.radio52, SIGNAL("clicked()"), self.radio52Clicked)
        vbox5 = QVBoxLayout()
        vbox5.addWidget(self.radio51)
        vbox5.addWidget(self.radio52)
        vbox5.addStretch(1)
        self.QGBox5.setLayout(vbox5)
				
		# creation du texEdit pour release
        self.QGBox6 = QGroupBox("release")
        self.lineedit1 = QLineEdit(self)
        self.lineedit1.setText(self.cmsenv.getCMSSWBASECMSSWVERSION()) # default
        self.lineedit1.setMinimumWidth(150)
        vbox6 = QVBoxLayout()
        vbox6.addWidget(self.lineedit1)
        self.QGBox6.setLayout(vbox6)

        #Layout intermédiaire : création et peuplement des gpes radios
        self.layoutH_radio = QHBoxLayout()
        self.layoutH_radio.addWidget(self.QGBox4)
        self.layoutH_radio.addWidget(self.QGBox0)
        self.layoutH_radio.addWidget(self.QGBox1)
        self.layoutH_radio.addWidget(self.QGBox31)
        self.layoutH_radio.addWidget(self.QGBox32)
        self.layoutH_radio.addStretch(1)
        self.layoutH_radio.addWidget(self.QGBox5)
        self.layoutH_radio.addWidget(self.QGBox2)
        self.layoutH_radio.addWidget(self.QGBox6)

		# creation du label resumé
        self.labelResume = QLabel(self.trUtf8(self.texte), self)
		# creation du grpe Folders paths
        self.QGBox8 = QGroupBox("Folders paths")
        vbox8 = QVBoxLayout()
        vbox8.addWidget(self.labelResume)
        self.QGBox8.setLayout(vbox8)

        #creation du TextEdit pour affichage
        self.edit = QTextEdit(self)
        self.edit.setMinimumHeight(300)

        # Création du bouton quitter, ayant pour parent la "fenetre"
        self.boutonQ = QPushButton(self.trUtf8("Quitter ?"),self)
        self.boutonQ.setFont(QFont("Comic Sans MS", 14,QFont.Bold,True))
        self.boutonQ.setIcon(QIcon("../images/smile.png"))
        self.connect(self.boutonQ, SIGNAL("clicked()"), qApp, SLOT("quit()"))

        # Création du bouton Test, ayant pour parent la "fenetre"
        self.bouton3 = QPushButton(self.trUtf8("Go !"),self)
        self.bouton3.setFont(QFont("Comic Sans MS", 14,QFont.Bold,True))
        self.bouton3.setIcon(QIcon("../images/smile.png"))
        self.connect(self.bouton3, SIGNAL("clicked()"), self.liste3) 

        #Layout intermédiaire : boutons
        self.layoutH_boutons = QHBoxLayout()
        self.layoutH_boutons.addWidget(self.bouton3)
        self.layoutH_boutons.addStretch(1)
        self.layoutH_boutons.addWidget(self.boutonQ)

        #Layout intermédiaire : ComboBox + labelcombo
        self.layoutV_combobox = QVBoxLayout()
        self.layoutV_combobox.addWidget(self.QGBox8)
        
        # creation des onglets
        self.onglets = QTabWidget()
        self.generalTab = QWidget()
        self.onglets.insertTab(0, self.generalTab, "General")
        #Set Layout for Tabs Pages
        self.generalTab.setLayout(self.layoutV_combobox)   

        #Layout principal : création et peuplement
        self.layout_general = QVBoxLayout()
        self.layout_general.addLayout(self.layoutH_radio)
        self.layout_general.addWidget(self.onglets)
        self.layout_general.addWidget(self.edit)
        self.layout_general.addLayout(self.layoutH_boutons)
        self.setLayout(self.layout_general)

    def liste3(self):
        # extraction du texte depuis text edit 2
        texte_release = self.lineedit1.text()
        print "texte : ", texte_release
        
        if self.radio21.isChecked():
            print "-- store"
            self.edit.append("-- store")
        if self.radio22.isChecked():
            print "-- force"
            self.edit.append("-- force")
        print "-----"
        QtCore.QCoreApplication.processEvents()
        
        # choix interaction
        if self.radio41.isChecked():
            self.choix_interaction = './electronBsub ' + self.choix_job + ' /afs/cern.ch/cms/utils/oval run ' + self.choix_etape + '.Val'
        if self.radio42.isChecked():
            self.choix_interaction = '/afs/cern.ch/cms/utils/oval run ' + self.choix_etape + '.Val'
        
#        print self.choix_interaction
        self.edit.append(self.choix_interaction)
        
        get_choix_calcul(self)        
        print "choix_calcul : ", self.choix_calcul
        self.edit.append(self.choix_calcul)
        
        # creation des repertoires
        cmd_folder_creation(self.choix_calcul)
        
        # if store is checked then copy of DQM*.root files
        if self.radio03.isChecked():
#            print "copie des fichiers DQM*.root to be done"
            copy_files(self)
        
        # liste collections to do (Pt35, Pt10, TTbar, ....)
        coll_list = get_collection_list(self)

        for items in coll_list: # to be removed
            self.edit.append(items)
            QtCore.QCoreApplication.processEvents()
        
        # work to execute
        if self.radio04.isChecked():     # publish
            print "publish to be done"
            if self.radio13.isChecked(): # FAST
                print "Fast & publish to be done"
                for val_Fast in ['VsFull', 'VsFast']:
                    for items in coll_list:
                        cmd = self.choix_interaction + self.choix_calcul + val_Fast + items + '_gedGsfE'
                        self.edit.append(cmd)
                        QtCore.QCoreApplication.processEvents()                
                        subprocess.call(cmd, shell = True)
            else:                        # no FAST
                print "no Fast & publish to be done"
                for items in coll_list:
                    cmd = self.choix_interaction + self.choix_calcul + items + '_gedGsfE'
                    self.edit.append(cmd)
                    QtCore.QCoreApplication.processEvents()
                    subprocess.call(cmd, shell = True)
            
            # rm dd*.olog dqm*.root 
            clean_files(self)
        else:
            print "no publish : general case"
            for items in coll_list:
                cmd = self.choix_interaction + self.choix_calcul + items + '_gedGsfE'
                self.edit.append(cmd)
                QtCore.QCoreApplication.processEvents()
                subprocess.call(cmd, shell = True)

            
        # end
                
#        print "liste : "
#        toto = liste()
#        QtCore.QCoreApplication.processEvents()
#        for items in toto:
#            self.edit.append(items)
#            QtCore.QCoreApplication.processEvents()
            
#        self.edit.append(self.choix_calcul)
#        QtCore.QCoreApplication.processEvents()
        
#        subprocess.call("./boucle.tcsh &", shell = True)
        print "fin"

        
    def radio01Clicked(self):
        if self.radio01.isChecked():
            self.QGBox2.setEnabled(False)
            self.QGBox2.setVisible(False)
            self.choix_etape = 'analyze' # default
            self.choix_calcul = 'Full'
        QtCore.QCoreApplication.processEvents()

    def radio02Clicked(self):
        if self.radio02.isChecked():
            self.QGBox2.setEnabled(False)
            self.QGBox2.setVisible(False)
            self.choix_etape = 'finalize' # default
            self.choix_calcul = 'Full'
        QtCore.QCoreApplication.processEvents()
        
    def radio03Clicked(self):
        if self.radio03.isChecked():
            self.QGBox2.setEnabled(True)
            self.QGBox2.setVisible(True)
            self.choix_etape = 'store' # default
            self.choix_calcul = 'Full'
        QtCore.QCoreApplication.processEvents()

    def radio04Clicked(self):
        if self.radio04.isChecked():
            self.QGBox2.setEnabled(False)
            self.QGBox2.setVisible(False)
            self.choix_etape = 'publish' # default
            self.choix_calcul = 'gedvsgedFull'
        QtCore.QCoreApplication.processEvents()
        
    def radio11Clicked(self):
        if self.radio11.isChecked():
            self.QGBox31.setVisible(True)
            self.QGBox32.setVisible(False)
            self.choix_calcul = 'Full'
        QtCore.QCoreApplication.processEvents()

    def radio12Clicked(self):
        if self.radio12.isChecked():
            self.QGBox31.setVisible(False)
            self.QGBox32.setVisible(True)
            self.choix_calcul = 'PileUp'
        QtCore.QCoreApplication.processEvents()
        
    def radio13Clicked(self):
        if self.radio13.isChecked():
            self.QGBox31.setVisible(False)
            self.QGBox32.setVisible(True)
            self.choix_calcul = 'Fast'
        QtCore.QCoreApplication.processEvents()
        
    def radio21Clicked(self):
        if self.radio21.isChecked():
            self.choix_etape = 'store'
        QtCore.QCoreApplication.processEvents()

    def radio22Clicked(self):
        if self.radio22.isChecked():
            self.choix_etape = 'force'
        QtCore.QCoreApplication.processEvents()
        
    def radio41Clicked(self):
        if self.radio41.isChecked():
            self.QGBox5.setEnabled(True)
            self.QGBox5.setVisible(True)
        QtCore.QCoreApplication.processEvents()

    def radio42Clicked(self):
        if self.radio42.isChecked():
            self.QGBox5.setEnabled(False)
            self.QGBox5.setVisible(False)
        QtCore.QCoreApplication.processEvents()
        
    def radio51Clicked(self):
        if self.radio51.isChecked():
            self.choix_job = '8nh'
        QtCore.QCoreApplication.processEvents()

    def radio52Clicked(self):
        if self.radio52.isChecked():
            self.choix_job = '1nh'
        QtCore.QCoreApplication.processEvents()
