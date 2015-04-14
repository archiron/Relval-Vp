#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

import os,sys,subprocess

from getEnv import env
from fonctions import cmd_test, liste, cmd_folder_creation, get_collection_list, get_choix_calcul, clean_files, copy_files, cmd_fetch, cmd_relval, cmd_listeRECO, cmd_listeDQM, list_search, explode_item
from fonctions import list_simplify, write_OvalFile, create_file_list, create_commonfile_list
from getChoice import *
from getPublish import *
		
#############################################################################
class ovalGui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('DQMGui publish v0.8.0')

        self.cmsenv = env()
        self.texte = self.cmsenv.cmsAll()
        self.choix_calcul = 'Full'   # default
        self.choice_rel = ""
        self.choice_ref = ""
        self.coll_list = []
        self.files_list = []
        self.my_choice_rel = "" # for transmission data between the 2 windows
        self.my_choice_ref = "" # for transmission data between the 2 windows
						
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
        				
		# creation du grpe liste des collections
        self.QGBox31 = QGroupBox("Data Sets")
        self.QGBox32 = QGroupBox("Data Sets")
        self.QGBox31.setMaximumHeight(150)
        self.QGBox32.setMaximumHeight(150)
        self.QGBox31.setVisible(True)
        self.QGBox32.setVisible(False)
        self.check31 = QCheckBox("Pt10Startup_UP15")
        self.check32 = QCheckBox("Pt35Startup_UP15")
        self.check33 = QCheckBox("Pt1000Startup_UP15")
        self.check34 = QCheckBox("QcdPt80120Startup_13") # ex QcdPt80Pt120Startup_13
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
        qform31 = QFormLayout() # new
        qform31.addRow(self.check31, self.check32) # new
        qform31.addRow(self.check33, self.check34) # new
        qform31.addRow(self.check35, self.check36) # new
        self.QGBox31.setLayout(qform31) # new
        qform32 = QFormLayout() # new
        qform32.addRow(self.check37, self.check38) # new
        self.QGBox32.setLayout(qform32) # new
        
		# creation du grpe All/None
        self.QGBoxAllNone = QGroupBox("All / None")
        self.QGBoxAllNone.setMaximumHeight(150)
        self.QGBoxAllNone.setMinimumHeight(150)
        self.checkAllNone1 = QRadioButton("All")
        self.checkAllNone2 = QRadioButton("None")
        self.checkAllNone1.setChecked(True)
        self.connect(self.checkAllNone1, SIGNAL("clicked()"), self.checkAllNone1Clicked)
        self.connect(self.checkAllNone2, SIGNAL("clicked()"), self.checkAllNone2Clicked)
        vboxAllNone = QVBoxLayout()
        vboxAllNone.addWidget(self.checkAllNone1)
        vboxAllNone.addWidget(self.checkAllNone2)
        vboxAllNone.addStretch(1)
        self.QGBoxAllNone.setLayout(vboxAllNone)
                				
		# creation des texEdit pour release/reference
        self.QGBox6 = QGroupBox("release")
        self.lineedit1 = QLineEdit(self)
        self.lineedit1.setText(self.cmsenv.getCMSSWBASECMSSWVERSION()) # default
        self.lineedit1.setMinimumWidth(150)
        self.lineedit3 = QLineEdit(self)
        self.lineedit3.setText(self.cmsenv.getCMSSWBASECMSSWVERSION()) # the same by default
        self.lineedit3.setMinimumWidth(150)
        self.label61 = QLabel("release", self)
        self.label61.setMaximumWidth(80)
        self.label61.setMinimumWidth(80)
        self.label62 = QLabel("reference", self)
        self.label62.setMaximumWidth(80)
        self.label62.setMinimumWidth(80)
        hbox61 = QHBoxLayout()
        hbox61.addWidget(self.label61)
        hbox61.addWidget(self.lineedit1)
        hbox62 = QHBoxLayout()
        hbox62.addWidget(self.label62)
        hbox62.addWidget(self.lineedit3)
        vbox6 = QVBoxLayout()
        vbox6.addLayout(hbox61)
        vbox6.addLayout(hbox62)
        vbox6.addStretch(1)
        self.QGBox6.setLayout(vbox6)

        #Layout intermédiaire : création et peuplement des gpes radios
        self.layoutH_radio = QHBoxLayout()
        self.layoutH_radio.addWidget(self.QGBox1)
        self.layoutH_radio.addWidget(self.QGBox31)
        self.layoutH_radio.addWidget(self.QGBox32)
        self.layoutH_radio.addWidget(self.QGBoxAllNone)
        self.layoutH_radio.addStretch(1)
        self.layoutH_radio.addWidget(self.QGBox6)

        # Création du bouton Get choice !, ayant pour parent la "fenetre"
        self.bouton3 = QPushButton(self.trUtf8("Get choice !"),self)
        self.bouton3.setFont(QFont("Comic Sans MS", 14,QFont.Bold,True))
        self.bouton3.setIcon(QIcon("../images/smile.png"))
        self.connect(self.bouton3, SIGNAL("clicked()"), self.liste4) 

        # Création du bouton Get files !, ayant pour parent la "fenetre"
        self.bouton5 = QPushButton(self.trUtf8("Get files !"),self)
        self.bouton5.setFont(QFont("Comic Sans MS", 14,QFont.Bold,True))
        self.bouton5.setIcon(QIcon("../images/smile.png"))
        self.connect(self.bouton5, SIGNAL("clicked()"), self.liste5) 
        self.bouton5.setEnabled(False)

        # Création du bouton Publish config, ayant pour parent la "fenetre"
        self.bouton6 = QPushButton(self.trUtf8("Publish config"),self)
        self.bouton6.setFont(QFont("Comic Sans MS", 14,QFont.Bold,True))
        self.bouton6.setIcon(QIcon("../images/smile.png"))
        self.connect(self.bouton6, SIGNAL("clicked()"), self.liste6) 

        # Création du bouton Publish !, ayant pour parent la "fenetre"
        self.bouton4 = QPushButton(self.trUtf8("Publish !"),self)
        self.bouton4.setFont(QFont("Comic Sans MS", 14,QFont.Bold,True))
        self.bouton4.setIcon(QIcon("../images/smile.png"))
        self.connect(self.bouton4, SIGNAL("clicked()"), self.liste3) 

        # Création du bouton quitter, ayant pour parent la "fenetre"
        self.boutonQ = QPushButton(self.trUtf8("Quitter ?"),self)
        self.boutonQ.setFont(QFont("Comic Sans MS", 14,QFont.Bold,True))
        self.boutonQ.setIcon(QIcon("../images/smile.png"))
        self.connect(self.boutonQ, SIGNAL("clicked()"), qApp, SLOT("quit()"))
        
        #Layout intermédiaire : boutons
        self.layoutH_boutons = QHBoxLayout()
        self.layoutH_boutons.addWidget(self.bouton3)
        self.layoutH_boutons.addWidget(self.bouton5)
        self.layoutH_boutons.addWidget(self.bouton6)
        self.layoutH_boutons.addWidget(self.bouton4)
        self.layoutH_boutons.addStretch(1)
        self.layoutH_boutons.addWidget(self.boutonQ)

		# creation du label resumé
        self.labelResume = QLabel(self.trUtf8(self.texte), self)
		# creation du grpe Folders paths
        self.QGBox8 = QGroupBox("Folders paths")
        vbox8 = QVBoxLayout()
        vbox8.addWidget(self.labelResume)
        self.QGBox8.setLayout(vbox8)

        #Layout intermédiaire : ComboBox + labelcombo
        self.layoutV_combobox = QVBoxLayout()
        self.layoutV_combobox.addWidget(self.QGBox8)
        
        # creation des onglets
        self.onglets = QTabWidget()
        self.generalTab = QWidget()
        self.generalTab.setMinimumHeight(150)
        self.onglets.insertTab(0, self.generalTab, "General")
        #Set Layout for Tabs Pages
        self.generalTab.setLayout(self.layoutV_combobox)   

        #Layout principal : création et peuplement
        self.layout_general = QVBoxLayout()
        self.layout_general.addLayout(self.layoutH_radio)
        self.layout_general.addWidget(self.onglets)
        self.layout_general.addLayout(self.layoutH_boutons)
        self.setLayout(self.layout_general)

    def liste3(self):
        
        # step 1 : test if arborescence is OK Validation/RecoEgamma/test
        my_folder = os.getcwd()
        f_test = 'Validation/RecoEgamma/test'
#        print "my folder : ", my_folder
        if not f_test in my_folder:
#            print "pas bon"
            BoiteMessage = QMessageBox()
            BoiteMessage.setText("You must be in the Validation/RecoEgamma/test of the release to work.")
            BoiteMessage.setWindowTitle("WARNING !")
            BoiteMessage.exec_()
        else:
            # step 2 : create the OvalFile for the calcul (Full, Fast, PU) choice
        
            # choix interaction
            self.choix_interaction = '/afs/cern.ch/cms/utils/oval run publish.Val'
        
            get_choix_calcul(self)        
#            print "choix_calcul : ", self.choix_calcul
        
            # creation des repertoires
            self.folder_name = cmd_folder_creation(self.choix_calcul)
            for it in self.folder_name:
                print it
        
            # get collections list to do (Pt35, Pt10, TTbar, .... if checked)
            self.coll_list = get_collection_list(self)

            # work to execute
#            if self.radio04.isChecked():     # publish
            if self.radio13.isChecked(): # FAST
                print "Fast & publish"
                for val_Fast in ['VsFull', 'VsFast']:
                    for items in self.coll_list:
                        cmd = self.choix_interaction + self.choix_calcul + val_Fast + items + '_gedGsfE'
                        subprocess.call(cmd, shell = True)
            else:                        # no FAST
                print "no Fast & publish"
                for items in self.coll_list:
                    cmd = self.choix_interaction + self.choix_calcul + items + '_gedGsfE'
                    subprocess.call(cmd, shell = True)
            
            clean_files(self)

        print "fin"

    def liste4(self):
#        print "liste 4"
        # mettre la fonction liste3 du ovalGui de Projet_DQM-V2
        list_search(self)
        to_transmit = [str(self.lineedit1.text()), str(self.lineedit3.text()), self.rel_list, self.ref_list]
        self.getChoice_update(to_transmit)
        
    def liste5(self):
#        print "liste 5"
        # pour recuperer les fichiers DQM*.root
        # step 1 : si pas de release et/ou de reference : ne rien faire
        # step 2 : refaire une liste des fichiers a recuperer
        # step 3 : charger les fichiers (on passe le nom du fichier comme option -e="nom_fichier")
        # (liste_fichiers_3) = cmd_fetch(option_is_from_data, option_release_3, option_regexp, option_mthreads, option_dry_run)
#        print "liste 5 : coucou"
        if ( self.my_choice_rel ) :
#            print "self.choice_rel : ", self.choice_rel
            if ( self.my_choice_ref ) :
#                print "self.choice_ref : ", self.choice_ref 
                # Normalement ce double test est déjà fait
                # il faudrait vérifier si les cochés correspondent aux fichiers
                # step 1 : done
                option_is_from_data = "mc" # mc ou data
                option_mthreads = 3
                option_dry_run = False # False telecharge , True liste

                itl2 = create_file_list(self.choice_rel)
                itf2 = create_file_list(self.choice_ref)
                
                self.files_list = create_commonfile_list(itl2, itf2) # attention on ne compare pas la longueur des tableaux
#                print self.files_list
                
                # step 2 : done
                option_release_rel = str(self.choice_rel[0]) 
                for part_rel_3 in itl2:
                    option_regexp_rel = str( part_rel_3[1] ) 
                    cmd_fetch(option_is_from_data, option_release_rel, option_regexp_rel, option_mthreads, option_dry_run)

                option_release_ref = str(self.choice_ref[0]) 
                for part_ref_3 in itf2:
                    option_regexp_ref = str( part_ref_3[1] ) 
                    cmd_fetch(option_is_from_data, option_release_ref, option_regexp_ref, option_mthreads, option_dry_run)
                # step 3 : done
                tmp = self.labelResume.text()
                tmp += "<br /><strong>All files loaded.</strong>"
                self.labelResume.setText(tmp)
                QtCore.QCoreApplication.processEvents()

            else:
                print "no reference choosed. Nothing to do."
        else:
            print "no release choosed. Nothing to do."
         
    def liste6(self):
#        print "liste 6"

        name_rel_p = ( self.lineedit1.text(), '', '' ) # default
        name_ref_p = ( self.lineedit3.text(), '', '' ) # default
        if ( self.my_choice_rel ) :
#            print "self.choice_rel : ", self.choice_rel
            if ( self.my_choice_ref ) :
#                print "self.choice_ref : ", self.choice_ref
                name_rel_p = self.choice_rel
                name_ref_p = self.choice_ref
        to_transmit = [name_rel_p, name_ref_p]
        self.getPublish_update(to_transmit)
        
    def getChoice_update(self, to_transmit):
        from operator import itemgetter
        """Lance la deuxième fenêtre"""
        self.getChoice = GetChoice()
        
        self.rel_list_mod = []
        self.ref_list_mod = []
        self.rel_list_mod2 = []
        self.ref_list_mod2 = []
    
#        print "longueur tablo to_transmit[2] : ", len(to_transmit[2])
#        print "longueur tablo to_transmit[3] : ", len(to_transmit[3])
        if ( len(to_transmit[2]) == 0): # release empty
#            print "pas bon"
            BoiteMessage = QMessageBox()
            BoiteMessage.setText("There is no data release.")
            BoiteMessage.setWindowTitle("WARNING !")
            BoiteMessage.exec_()
        else: # release data OK
            if ( len(to_transmit[3]) == 0): # reference empty
                BoiteMessage = QMessageBox()
                BoiteMessage.setText("There is no data reference to compare.")
                BoiteMessage.setWindowTitle("WARNING !")
                BoiteMessage.exec_()
            else: # release and reference are OK
                self.getChoice.bouton.setText("Quit") # to be removed ?
                for items in to_transmit[2]:
                    items3 = explode_item(items)
                    items4 = (items3[1], items3[2], items3[0])
                    self.rel_list_mod.append(items4)
                for items in to_transmit[3]:
                    items3 = explode_item(items)
                    items4 = (items3[1], items3[2], items3[0])
                    self.ref_list_mod.append(items4)
            
                list_tmp = sorted(self.rel_list_mod, key=itemgetter(0,1), reverse=True)
                self.rel_list_mod = list_tmp
                list_tmp = sorted(self.ref_list_mod, key=itemgetter(0,1), reverse=True)
                self.ref_list_mod = list_tmp
        
#                print "release tablo avant : ", self.rel_list_mod
#                print "longueur tablo : ", len(self.rel_list_mod)
                self.rel_list_mod2 = list_simplify(self.rel_list_mod)
#                print "release retour tablo : ", self.rel_list_mod2
#                print "reference tablo avant : ", self.ref_list_mod
#                print "longueur tablo : ", len(self.ref_list_mod)
                self.ref_list_mod2 = list_simplify(self.ref_list_mod)
#                print "reference retour tablo : ", self.ref_list_mod2

                i = 0
                k = 0
                self.buttons_rel = []
                for items in self.rel_list_mod2:
                    it1 = ''
                    it2 = items[2]
                    for it in it2:
#                        print "+-+-+-", it
                        it1 += it + ', '
                    it1 = it1[0:len(it1)-2]
                    items = (items[0], items[1], it1)
                    j = 0
                    for items2 in items:
                        if ( j == 1 ):
                            t = QRadioButton(items2)
                        else: # j = 2
                            t = QLabel(items2)
                        self.buttons_rel.append(t)
                        self.getChoice.gbox_H1.addWidget(self.buttons_rel[i], k, j)
                        self.connect(self.buttons_rel[i], SIGNAL("clicked()"), self.buttons_relClicked)
                        j += 1
                        i += 1
                    k += 1           
            
                i = 0
                k = 0
                self.buttons_ref = []
                for items in self.ref_list_mod2:
                    it1 = ''
                    it2 = items[2]
                    for it in it2:
                        it1 += it + ', '
                    it1 = it1[0:len(it1)-2]
                    items = (items[0], items[1], it1)
                    j = 0
                    for items2 in items:
                        if ( j == 1 ):
                            t = QRadioButton(items2)
                        else: # j = 2
                            t = QLabel(items2)
                        self.buttons_ref.append(t)
                        self.getChoice.gbox_H2.addWidget(self.buttons_ref[i], k, j)
                        self.connect(self.buttons_ref[i], SIGNAL("clicked()"), self.buttons_refClicked)
                        j += 1
                        i += 1
                    k += 1           
            
                # en cas de signal "fermeturegetChoice()" reçu de self.getChoice => exécutera clienchoisi 
                self.connect(self.getChoice, SIGNAL("fermeturegetChoice(PyQt_PyObject)"), self.clientchoice) 
                # la deuxième fenêtre sera 'modale' (la première fenêtre sera inactive)
                self.getChoice.setWindowModality(QtCore.Qt.ApplicationModal)
                # appel de la deuxième fenêtre
                self.getChoice.show()

    def clientchoice(self, x):
        """affiche le résultat x transmis par le signal à l'arrêt de la deuxième fenêtre"""
        tmp = self.trUtf8(self.texte) 
        tmp += "<br /><strong>Release : </strong>"
        if ( self.my_choice_rel ) :
            tmp += str(self.my_choice_rel)
#            self.choice_rel = self.my_choice_rel
        tmp += "<br /><strong>Reference : </strong>"
        if ( self.my_choice_ref ) :
            tmp += str(self.my_choice_ref)
        self.labelResume.setText(tmp)
        QtCore.QCoreApplication.processEvents()
        print "recup = ", x # to be removed
        self.bouton5.setEnabled(False)
        if ( self.my_choice_rel ) :
#            print "self.choice_rel : ", self.choice_rel
            if ( self.my_choice_ref ) :
#                print "self.choice_ref : ", self.choice_ref 
                self.bouton5.setEnabled(True)

    def buttons_relClicked(self):
        i = 0
        k = 0
        for items in self.rel_list_mod2:
            j = 0
            for items2 in items:
                if ( j == 1 ):
                    if self.buttons_rel[i].isChecked():
                        self.my_choice_rel = self.rel_list_mod2[k]
                        self.choice_rel = self.rel_list_mod2[k]
#                        print self.buttons_rel[i].text(), " checked with (%i, %i, %i)", i, j, k
#                        print self.buttons_rel[i].text(), " checked with ", self.rel_list_mod2[k]
                j += 1
                i += 1
            k += 1
        QtCore.QCoreApplication.processEvents()

    def buttons_refClicked(self):
        i = 0
        k = 0
        for items in self.ref_list_mod2:
            j = 0
            for items2 in items:
                if ( j == 1 ):
                    if self.buttons_ref[i].isChecked():
                        self.my_choice_ref = self.ref_list_mod2[k]
                        self.choice_ref = self.ref_list_mod2[k]
#                        print self.buttons_ref[i].text(), " checked with (%s, %s, %s)", i, j, k
#                        print self.buttons_ref[i].text(), " checked with ", self.ref_list_mod2[k]
                j += 1
                i += 1
            k += 1
        QtCore.QCoreApplication.processEvents()
                
    def getPublish_update(self, to_transmit):
        from operator import itemgetter
        """Lance la troisième fenêtre"""
        self.getPublish = GetPublish()
           
        self.getPublish.bouton_P.setText("Quit") # to be removed ?

#        for items in to_transmit:
#            print "Publish : ", items
        self.getPublish.to_transmit = to_transmit

        self.getPublish.transmit_rel = to_transmit[0][0]
        self.getPublish.transmit_ref = to_transmit[1][0]
#        print self.getPublish.transmit_rel
        
        if ( to_transmit[0][1] == "" ): # release globaltag empty
            BoiteMessage = QMessageBox()
            BoiteMessage.setText("There is no data release to make for OvalFile.")
            BoiteMessage.setWindowTitle("WARNING !")
            BoiteMessage.exec_()
        else: # data release OK
            if ( to_transmit[1][1] == "" ): # reference globaltag empty
                BoiteMessage = QMessageBox()
                BoiteMessage.setText("There is no data reference to make for OvalFile.")
                BoiteMessage.setWindowTitle("WARNING !")
                BoiteMessage.exec_()
            else:  # release and reference globaltag OK
                self.getPublish.t_rel.setText('release : ' + to_transmit[0][0])
                self.getPublish.t_ref.setText('reference : ' + to_transmit[1][0])
                self.getPublish.test_new.setText('test new : ' + self.getPublish.transmit_rel[6:])
                self.getPublish.test_ref.setText('test ref : ' + self.getPublish.transmit_ref[6:])
                
                (tag_startup, data_version) = to_transmit[0][1].split('-')
#                print "tag_startup : ",tag_startup
#                print "data_version : ", data_version
#                print self.gccs
                if self.gccs == 'Fast':
                    tag_startup = tag_startup[:-8]
                if self.gccs == 'PU':
                    tag_startup = tag_startup[7:]
                self.getPublish.tag_startup.setText('Tag Startup : ' + tag_startup) # pbm with fastsim_ pu PU25(50)ns_ get choix calcul -> done
                self.getPublish.data_version.setText('Data Version : ' + data_version)
                self.getPublish.lineEdit.setText('File to be created')
                
                # insert the web folder name            
                t_rel_default_text = to_transmit[0][0][6:] + self.getPublish.text_ext
                self.getPublish.t_rel_default.setText("Default web folder name : " + t_rel_default_text)
        
                self.Oval_OK = False
                self.Oval_OK = write_OvalFile(self, t_rel_default_text, to_transmit[0][1])

        
                # en cas de signal "fermeturegetPublish()" reçu de self.getPublish => exécutera clienchoisi 
                self.connect(self.getPublish, SIGNAL("fermeturegetPublish(PyQt_PyObject)"), self.clientpublish) 
                # la deuxième fenêtre sera 'modale' (la première fenêtre sera inactive)
                self.getPublish.setWindowModality(QtCore.Qt.ApplicationModal)
                # appel de la deuxième fenêtre
                self.getPublish.show()

    def clientpublish(self, x):
        """affiche le résultat x transmis par le signal à l'arrêt de la deuxième fenêtre"""
        if self.Oval_OK:
            print "True"
        else:
            print "False"
        tmp = self.labelResume.text()
        tmp += "<br /><strong>OvalFile created</strong>"
        self.labelResume.setText(tmp)
        QtCore.QCoreApplication.processEvents()
        print "recup2 = ", x # to be removed
        
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
                        
    def checkAllNone1Clicked(self):
        if self.checkAllNone1.isChecked():
#            print "All"
            self.check31.setChecked(True)
            self.check32.setChecked(True)
            self.check33.setChecked(True)
            self.check34.setChecked(True)
            self.check35.setChecked(True)
            self.check36.setChecked(True)
            self.check37.setChecked(True)
            self.check38.setChecked(True)
        QtCore.QCoreApplication.processEvents() 

    def checkAllNone2Clicked(self):
        if self.checkAllNone2.isChecked():
#            print "None"
            self.check31.setChecked(False)
            self.check32.setChecked(False)
            self.check33.setChecked(False)
            self.check34.setChecked(False)
            self.check35.setChecked(False)
            self.check36.setChecked(False)
            self.check37.setChecked(False)
            self.check38.setChecked(False)
        QtCore.QCoreApplication.processEvents() 
        