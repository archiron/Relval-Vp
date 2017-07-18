#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

import os,sys,subprocess

from getEnv import env
from fonctions import cmd_test, liste, cmd_folder_creation, get_collection_list, get_choix_calcul, clean_files, copy_files, cmd_fetch, cmd_relval, cmd_listeRECO, cmd_listeDQM, list_search, explode_item
from fonctions import list_simplify, write_OvalFile, create_file_list, create_commonfile_list, cmd_working_dirs_creation
from getChoice import *
from getPublish import *
		
#############################################################################
class ovalGui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('DQMGui publish v1.0.6.0') # use of self.FastvsFastTag and self.FastvsFullTag in order to avoid file manipulation "by hand" after publishing

        self.cmsenv = env()
        self.texte = self.cmsenv.cmsAll()
        self.choix_calcul = 'Full'   # default
        self.choice_rel = ""
        self.choice_ref = ""
        self.coll_list = []
        self.files_list = []
        self.my_choice_rel = "" # for transmission data between the 2 windows
        self.my_choice_ref = "" # for transmission data between the 2 windows
        self.working_dir_base = os.getcwd()
        self.working_dir_rel = os.getcwd()
        self.working_dir_ref = os.getcwd()
						
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
        self.check31 = QCheckBox("Pt10Startup_UP15") #
        self.check32 = QCheckBox("Pt35Startup_UP15") #
        self.check33 = QCheckBox("Pt1000Startup_UP15") #
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
                				
		# creation du grpe RECO/MiniAOD
        self.QGBoxRECOMiniAOD = QGroupBox("RECO / MiniAOD / pmx")
        self.QGBoxRECOMiniAOD.setMaximumHeight(150)
        self.QGBoxRECOMiniAOD.setMinimumHeight(150)
        self.checkRECOMiniAOD1 = QRadioButton("RECO")
        self.checkRECOMiniAOD2 = QRadioButton("MiniAOD")
        self.checkRECOMiniAOD3 = QRadioButton("pmx")
        self.checkRECOMiniAOD1.setChecked(True)
        self.connect(self.checkRECOMiniAOD1, SIGNAL("clicked()"), self.checkRECOMiniAOD1Clicked)
        self.connect(self.checkRECOMiniAOD2, SIGNAL("clicked()"), self.checkRECOMiniAOD2Clicked)
        self.connect(self.checkRECOMiniAOD3, SIGNAL("clicked()"), self.checkRECOMiniAOD3Clicked)
        vboxRECOMiniAOD = QVBoxLayout()
        vboxRECOMiniAOD.addWidget(self.checkRECOMiniAOD1)
        vboxRECOMiniAOD.addWidget(self.checkRECOMiniAOD2)
        vboxRECOMiniAOD.addWidget(self.checkRECOMiniAOD3)
        vboxRECOMiniAOD.addStretch(1)
        self.QGBoxRECOMiniAOD.setLayout(vboxRECOMiniAOD)
                				
		# creation des texEdit pour release/reference
        self.QGBox6 = QGroupBox("release")
        self.QGBox6.setMaximumHeight(150)
        self.QGBox6.setMinimumHeight(150)
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
        self.layoutH_radio.addWidget(self.QGBoxRECOMiniAOD)
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
        self.boutonQ = QPushButton(self.trUtf8("Quit ?"),self)
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
        self.generalTab.setMinimumHeight(170)
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
        import os
        # step 1 : test if arborescence is OK Validation/RecoEgamma/test
        my_folder = os.getcwd()
        f_test = 'Validation/RecoEgamma/test'
#        print "liste3 Publish"
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
        
            # creation des repertoires
            cmd_working_dirs_creation(self)
            if not os.path.exists(self.working_dir_rel):
                print "working dir does not exist - END" # going to base folder
            else :
                self.folder_name = cmd_folder_creation(self.choix_calcul, self.working_dir_rel )
        
                # get collections list to do (Pt35, Pt10, TTbar, .... if checked)
                self.coll_list = get_collection_list(self)

                # TEMPORAIRE TEST REVIENT DE RELEASE FOLDER POUR TRAVAIL
#                print "liste 3 - current working directory : ", os.getcwd()      # Return the current working directory
                os.chdir(self.working_dir_base)   # Change current working directory to base directory
                print "WORKING DIR : ", os.getcwd()

                # work to execute
#                if self.radio04.isChecked():     # publish
                if self.radio13.isChecked(): # FAST
                    print "Fast & publish"
                    for val_Fast in ['VsFull', 'VsFast']:
                        for items in self.coll_list:
                            cmd = self.choix_interaction + self.choix_calcul + val_Fast + items + '_gedGsfE'
                            subprocess.call(cmd, shell = True)
                else:                        # no FAST
                    print "no Fast & publish"
                    for items in self.coll_list:
                        print items
                        cmd = self.choix_interaction + self.choix_calcul + items + '_gedGsfE'
                        print cmd
                        subprocess.call(cmd, shell = True)
            
                # TEMPORAIRE TEST REPASSE DANS RELEASE FOLDER
#                if not os.path.exists(str(self.lineedit1.text()[6:])):
#                    print "liste 3 - Creation of %s folder" % (str(self.lineedit1.text()[6:]))
#                    os.makedirs(str(self.lineedit1.text()[6:]))
#                print "liste 3 - current working directory : ", os.getcwd()      # Return the current working directory
#                os.chdir(str(self.lineedit1.text()[6:]))   # Change current working directory
                os.chdir(self.working_dir_rel)   # Change current working directory to release directory
#                print "liste 3 - current working directory : ", os.getcwd()      # Return the current working directory

                # clean dqm*.root and dd*.olog files. Copy other .root, .olog files and OvalFile into self.folder_name
                clean_files(self)
                
                tmp = self.labelResume.text()
                tmp += "<br /><strong>Publish done.</strong>"
                self.labelResume.setText(tmp)

        print "fin"

    def liste4(self):
        cmd_working_dirs_creation(self)
#        print "liste 4 Get Choice"
        
        if not os.path.exists(self.working_dir_rel):
            os.chdir(self.working_dir_base) # going to base folder
            print "liste 4 - Creation of (%s) folder" % str(self.lineedit1.text()[6:])
            os.makedirs(str(self.lineedit1.text()[6:]))
#        print "liste 4 - current working directory : ", os.getcwd()      # Return the current working directory, = base
        os.chdir(self.working_dir_rel)   # Change current working directory
        if not os.path.exists(self.working_dir_ref):
            print "liste 4 - Creation of (%s) folder" % str(self.lineedit3.text()[6:])
            os.makedirs(str(self.lineedit3.text()[6:]))
        list_search(self)
        to_transmit = [str(self.lineedit1.text()), str(self.lineedit3.text()), self.rel_list, self.ref_list]
        self.getChoice_update(to_transmit)
        
    def liste5(self):
#        print "liste 5 Get Files"

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

                print "liste5 - choice_rel : ", self.choice_rel
                print "liste5 - choice_ref : ", self.choice_ref
                itl2 = create_file_list(self.choice_rel)
                itf2 = create_file_list(self.choice_ref)
                
                self.files_list = create_commonfile_list(itl2, itf2) # attention on ne compare pas la longueur des tableaux
                print "liste 5 - self.files_list : ", self.files_list
                print "liste 5 - itl2 : ", itl2
                print "liste 5 - itf2 : ", itf2
                
                # step 2 : done
                option_release_rel = str(self.choice_rel[0]) 
                actual_dir = os.getcwd() # get the actual directory
#                print "actual dir : ", actual_dir
                os.chdir(self.working_dir_rel)   # Change current working directory to release directory
#                print "working dir : ", os.getcwd()
                for part_rel_3 in itl2:
                    print "\npart_rel_3 : ", part_rel_3 # OK
                    option_regexp_rel = str( part_rel_3[1] ) 
#                    print "appel chargement files" # OK
                    cmd_fetch(option_is_from_data, option_release_rel, option_regexp_rel, option_mthreads, option_dry_run)
                    if self.gccs == 'Fast': # FASTSIM - same as in FastvsFull in write_OvalFile()
                        print "loading liste 5 : ", part_rel_3[1]
                        it_tmp = part_rel_3[1].replace('_FastSim', '')
                        option_regexp_rel = str( it_tmp ) 
#                        print "appel chargement files" # OK
                        cmd_fetch(option_is_from_data, option_release_rel, option_regexp_rel, option_mthreads, option_dry_run)

                option_release_ref = str(self.choice_ref[0]) 
                os.chdir(self.working_dir_ref)   # Change current working directory to release directory
                for part_ref_3 in itf2:
                    print "\npart_ref_3 : ", part_ref_3 # OK
                    option_regexp_ref = str( part_ref_3[1] ) 
#                    print "appel chargement files" # OK
                    cmd_fetch(option_is_from_data, option_release_ref, option_regexp_ref, option_mthreads, option_dry_run)

                os.chdir(actual_dir) # back to actual directory
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
        print "\ngetChoice_update - to_transmit : ", to_transmit
        
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
#                print "getChoice_update - to_transmit[2] : ", to_transmit[2]
                for items in to_transmit[2]:
#                    print "rel ", items
                    items3 = explode_item(items)
                    items4 = (items3[1], items3[2], items3[0], items)
#                    print "getChoice_update : ", items4
                    self.rel_list_mod.append(items4)
#                print "getChoice_update - to_transmit[3] : ", to_transmit[3]
                for items in to_transmit[3]:
#                    print "ref ", items
                    items3 = explode_item(items)
                    items4 = (items3[1], items3[2], items3[0], items)
#                    print "getChoice_update : ", items4
                    self.ref_list_mod.append(items4)
            
                list_tmp = sorted(self.rel_list_mod, key=itemgetter(0,1), reverse=True)
                self.rel_list_mod = list_tmp
                list_tmp = sorted(self.ref_list_mod, key=itemgetter(0,1), reverse=True)
                self.ref_list_mod = list_tmp
        
#                print "release tablo avant : " 
#                for it in self.rel_list_mod:   
#                    print it
                self.rel_list_mod2 = list_simplify(self.rel_list_mod)
#                print "release retour tablo : "               
#                for it in self.rel_list_mod2:
#                    print it

#                print "reference tablo avant : ", self.ref_list_mod
                self.ref_list_mod2 = list_simplify(self.ref_list_mod)
#                print "reference retour tablo : ", self.ref_list_mod2

                i = 0
                k = 0
                self.buttons_rel = []
                for items in self.rel_list_mod2:
#                    print "boutons : ", items
                    it1 = ''
                    it2 = items[2]
                    for it in it2:
#                        print "+-+-+-", it
                        it1 += it + ', '
                    it1 = it1[0:len(it1)-2]
                    items = (items[0], items[1], it1)
#                    print "new boutons :", items
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
            
                # en cas de signal "fermeturegetChoice()" reçu de self.getChoice => exécutera clienchoice 
                self.connect(self.getChoice, SIGNAL("fermeturegetChoice(PyQt_PyObject)"), self.clientchoice) 
                # la deuxième fenêtre sera 'modale' (la première fenêtre sera inactive)
                self.getChoice.setWindowModality(QtCore.Qt.ApplicationModal)
                # appel de la deuxième fenêtre
                self.getChoice.show()

    def clientchoice(self, x):
        """affiche le résultat x transmis par le signal à l'arrêt de la deuxième fenêtre"""
        tmp = self.trUtf8(self.texte) 
        tmp += "<br /><strong>Release : </strong>"
#        print "clientchoice : ", self.my_choice_rel
        if ( self.my_choice_rel ) :
            tmp += str(self.my_choice_rel[0]) # to not write self.my_choice_rel[3]
            tmp += ' - ' + str(self.my_choice_rel[1]) # to not write self.my_choice_rel[3]
            tmp += ' - ' + str(self.my_choice_rel[2]) # to not write self.my_choice_rel[3]
#            self.choice_rel = self.my_choice_rel
        tmp += "<br /><strong>Reference : </strong>"
        if ( self.my_choice_ref ) :
            tmp += str(self.my_choice_ref[0]) # to not write self.my_choice_ref[3]
            tmp += ' - ' + str(self.my_choice_ref[1]) # to not write self.my_choice_ref[3]
            tmp += ' - ' + str(self.my_choice_ref[2]) # to not write self.my_choice_ref[3]
        self.labelResume.setText(tmp)
        QtCore.QCoreApplication.processEvents()
        print "recup = ", x, "\n" # to be removed
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
#            print "buttons_relClicked : ", items
            items = (items[0], items[1], items[2])
#            print "buttons_relClicked : ", items
            for items2 in items:
#                print "%d - %d - %d" % (i, j, k)
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
            items = (items[0], items[1], items[2])
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
                if self.radio13.isChecked():
                    print "GetPublish : Fast"
                    self.getPublish.QGBoxFastSim_P.setVisible(True)
                else:
                    self.getPublish.QGBoxFastSim_P.setVisible(False)

                self.getPublish.t_rel.setText('release : ' + to_transmit[0][0])
                self.getPublish.t_ref.setText('reference : ' + to_transmit[1][0])
                self.getPublish.test_new.setText('test new : ' + self.getPublish.transmit_rel[6:])
                self.getPublish.test_ref.setText('test ref : ' + self.getPublish.transmit_ref[6:])
                self.getPublish.miniAOD = False
                if self.checkRECOMiniAOD2.isChecked():
                    self.getPublish.miniAOD = True
                self.getPublish.pmx = False
                if self.checkRECOMiniAOD3.isChecked():
                    self.getPublish.pmx = True
                
                (tag_startup, data_version) = to_transmit[0][1].split('-')
                if self.gccs == 'Fast':
                    tag_startup = tag_startup[:-8]
                if self.gccs == 'PU':
                    len_prefix = len(tag_startup.split('_')[0])+1
                    tag_startup = tag_startup[len_prefix:]
                self.getPublish.tag_startup.setText('Tag Startup : ' + tag_startup) # pbm with fastsim_ pu get choix calcul -> done
                self.getPublish.data_version.setText('Data Version : ' + data_version)
                self.getPublish.lineEditFastSim.setText(tag_startup + '-' + data_version) # FastSim
                self.FastvsFastTag = tag_startup + '-' + data_version

                t_rel_default_text = self.getPublish.to_transmit[0][0][6:]
                if self.checkRECOMiniAOD2.isChecked():
                    t_rel_default_text = t_rel_default_text + "_miniAOD"
                if self.checkRECOMiniAOD3.isChecked():
                    t_rel_default_text = t_rel_default_text + "_pmx"
                t_rel_default_text = t_rel_default_text + self.getPublish.text_ext
                print "getPublish_update - t_rel_default_text : ", self.getPublish.text_ext, t_rel_default_text
                self.getPublish.t_rel_default.setText('Default web folder name : ' + t_rel_default_text)
                
                # en cas de signal "fermeturegetPublish()" reçu de self.getPublish => exécutera clienpublish 
                self.connect(self.getPublish, SIGNAL("fermeturegetPublish(PyQt_PyObject)"), self.clientpublish) 
                # la deuxième fenêtre sera 'modale' (la première fenêtre sera inactive)
                self.getPublish.setWindowModality(QtCore.Qt.ApplicationModal)
                # appel de la deuxième fenêtre
                self.getPublish.show()                
                
    def clientpublish(self, x):
        import os,sys,re
        """affiche le résultat x transmis par le signal à l'arrêt de la deuxième fenêtre"""
#        print "clientpublish = ", x, "\n" # to be removed
        (a,b) = x.split(":")
#        print "clientpublish = ", a # to be removed
        self.FastvsFullTag = b
        print "clientpublish = ", self.FastvsFullTag # to be removed
        x = a
        tmp = self.labelResume.text()
        self.Oval_OK = False
#        t_rel_default_text = self.getPublish.to_transmit[0][0][6:] + self.getPublish.text_ext
#        t_rel_default_text = self.getPublish.to_transmit[0][0][6:]
        if ( x == "_" ):
            t_rel_default_text = self.getPublish.to_transmit[0][0][6:]
        if ( x != "_" ):
            t_rel_default_text = self.getPublish.to_transmit[0][0][6:] + x
        if self.checkRECOMiniAOD2.isChecked():
            if ( re.search('miniAOD', self.getPublish.text_ext) ):
                t_rel_default_text = t_rel_default_text # rien
            else:
                t_rel_default_text = t_rel_default_text + "_miniAOD"
        if self.checkRECOMiniAOD3.isChecked():
            if ( re.search('pmx', self.getPublish.text_ext) ):
                t_rel_default_text = t_rel_default_text # rien
            else:
                t_rel_default_text = t_rel_default_text + "_pmx"
        t_rel_default_text = t_rel_default_text + self.getPublish.text_ext
        
        self.Oval_OK = write_OvalFile(self, t_rel_default_text, self.getPublish.to_transmit[0][1], self.getPublish.to_transmit[1][1])
        if self.Oval_OK:
#            print "True"
            print "clientItem OvalGui - t_rel_default_text : ", self.getPublish.text_ext, t_rel_default_text
            tmp += "<br /><strong>OvalFile created</strong>"
        else:
#            print "False"
            tmp += "<br /><strong>OvalFile non created !</strong>"

        self.labelResume.setText(tmp)
            
        QtCore.QCoreApplication.processEvents()
   
    def radio11Clicked(self): # Full
        if self.radio11.isChecked():
            self.QGBox31.setVisible(True)
            self.QGBox32.setVisible(False)
            self.choix_calcul = 'Full'
            self.checkRECOMiniAOD1.setChecked(True)
        QtCore.QCoreApplication.processEvents()

    def radio12Clicked(self): # PileUp
        if self.radio12.isChecked():
            self.QGBox31.setVisible(False)
            self.QGBox32.setVisible(True)
            self.choix_calcul = 'PileUp'
        QtCore.QCoreApplication.processEvents()
        
    def radio13Clicked(self): # Fast
        if self.radio13.isChecked():
            self.QGBox31.setVisible(False)
            self.QGBox32.setVisible(True)
            self.choix_calcul = 'Fast'
            self.checkRECOMiniAOD1.setChecked(True)
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
        
    def checkRECOMiniAOD1Clicked(self):
        if self.checkRECOMiniAOD1.isChecked():
            print "RECO"
        QtCore.QCoreApplication.processEvents() 

    def checkRECOMiniAOD2Clicked(self):
        if self.checkRECOMiniAOD2.isChecked():
            print "MiniAOD"
            self.radio11.isChecked()
            self.QGBox31.setVisible(True)
            self.QGBox32.setVisible(False)
            self.choix_calcul = 'Full'
            self.radio11.setChecked(True)
        QtCore.QCoreApplication.processEvents() 
        
    def checkRECOMiniAOD3Clicked(self):
        if self.checkRECOMiniAOD3.isChecked():
            print "pmx"
            self.radio12.setChecked(True)
            self.QGBox31.setVisible(False)
            self.QGBox32.setVisible(True)
            self.choix_calcul = 'PileUp'
        QtCore.QCoreApplication.processEvents() 
        