#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

import os,sys,subprocess

from getEnv import env
from fonctions import cmd_test, liste, cmd_folder_creation, get_collection_list, get_choix_calcul, clean_files, copy_files, cmd_fetch, cmd_relval, cmd_listeRECO, cmd_listeDQM, list_search, explode_item
from fonctions import list_simplify
		
#############################################################################
class Quelclient(QWidget):
 
    def __init__(self, parent=None):
        super(Quelclient, self).__init__(parent)
        self.setWindowTitle("Files choice")
 
        # créer un lineEdit
        self.lineEdit = QLineEdit(self)
        self.QGBox_0 = QGroupBox("Files list")
        self.QGBox_0.setMinimumWidth(1000)
        vbox_0 = QVBoxLayout()
        vbox_0.addWidget(self.lineEdit)
        self.QGBox_0.setLayout(vbox_0)
        
        # QHBoxLayout + 2 QGroupBox
        self.QGBox_H1 = QGroupBox("Release list")
        self.TextEdit_H1 = QTextEdit(self)
        self.TextEdit_H1.append("Coucou ! \n")
        vbox_H1 = QVBoxLayout()
        vbox_H1.addWidget(self.TextEdit_H1)
        self.QGBox_H1.setLayout(vbox_H1)
        self.QGBox_H2 = QGroupBox("Reference list")
        self.TextEdit_H2 = QTextEdit(self)
        self.TextEdit_H2.append("Coucou ! \n")
        vbox_H2 = QVBoxLayout()
        vbox_H2.addWidget(self.TextEdit_H2)
        self.QGBox_H2.setLayout(vbox_H2)
        
        self.QGBox_H1b = QGroupBox("Release list b")
        self.gbox_H1 = QGridLayout()
        self.QGBox_H1b.setLayout(self.gbox_H1)
        self.QGBox_H2b = QGroupBox("Reference list b")
        self.gbox_H2 = QGridLayout()
        self.QGBox_H2b.setLayout(self.gbox_H2)

        vbox_H0 = QVBoxLayout()
        vbox_H0.addWidget(self.QGBox_H1)
        vbox_H0.addWidget(self.QGBox_H1b)
        vbox_H0.addWidget(self.QGBox_H2)
        vbox_H0.addWidget(self.QGBox_H2b)

        # créer un bouton
        self.bouton = QPushButton("Cancel", self)
        self.bouton.clicked.connect(self.ok_m)
        hbox_button = QHBoxLayout()
        hbox_button.addStretch(1)
        hbox_button.addWidget(self.bouton)
        # positionner les widgets dans la fenêtre
        posit = QVBoxLayout()
        posit.addWidget(self.QGBox_0)
        posit.addLayout(vbox_H0)
        posit.addLayout(hbox_button)

        self.setLayout(posit)
 
    def ok_m(self):
        # emettra un signal "fermeturequelclient()" avec l'argument cité
        self.emit(SIGNAL("fermeturequelclient(PyQt_PyObject)"), unicode(self.lineEdit.text())) 
        # fermer la fenêtre
        self.close()
 
#############################################################################
class ovalGui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('DQMGui publish v0.2.0')

        self.cmsenv = env()
        self.texte = self.cmsenv.cmsAll()
        self.choix_calcul = 'Full'   # default
        self.choix_job = '8nh'       # default
        self.choix_etape = 'analyze' # default
        self.choice_rel = ""
        self.choice_ref = ""
		
		# creation du grpe Etapes
        self.QGBox0 = QGroupBox("Etapes")
        self.QGBox0.setMaximumHeight(150)
        self.QGBox0.setMaximumWidth(100)
        self.radio01 = QRadioButton("analyze") # Liste par defaut
        self.radio02 = QRadioButton("finalize")
        self.radio03 = QRadioButton("store")
        self.radio04 = QRadioButton("publish")
        self.radio01.setEnabled(False) # non active
        self.radio02.setEnabled(False) # non active
        self.radio03.setEnabled(False) # non active
        self.radio04.setChecked(True)
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
        self.QGBox31 = QGroupBox("Data Sets")
        self.QGBox32 = QGroupBox("Data Sets")
        self.QGBox31.setMaximumHeight(150)
        self.QGBox32.setMaximumHeight(150)
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
        
		# creation du grpe store/force
        self.QGBox4 = QGroupBox("batch/interactif")
        self.QGBox4.setMaximumHeight(150)
        self.QGBox4.setMinimumHeight(150)
        self.QGBox4.setMaximumWidth(100)		
        self.radio41 = QRadioButton("batch") # par defaut
        self.radio41.setEnabled(False) # non active, always interative
        self.radio42 = QRadioButton("interactif")
        self.radio42.setChecked(True)
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
        self.QGBox5.setVisible(False)
				
		# creation du texEdit pour release/reference
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
        self.layoutH_radio.addWidget(self.QGBox4)
        self.layoutH_radio.addWidget(self.QGBox0)
        self.layoutH_radio.addWidget(self.QGBox1)
        self.layoutH_radio.addWidget(self.QGBox31)
        self.layoutH_radio.addWidget(self.QGBox32)
        self.layoutH_radio.addWidget(self.QGBoxAllNone)
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

        # Création du bouton quitter, ayant pour parent la "fenetre"
        self.boutonQ = QPushButton(self.trUtf8("Quitter ?"),self)
        self.boutonQ.setFont(QFont("Comic Sans MS", 14,QFont.Bold,True))
        self.boutonQ.setIcon(QIcon("../images/smile.png"))
        self.connect(self.boutonQ, SIGNAL("clicked()"), qApp, SLOT("quit()"))

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

        # Création du bouton Publish !, ayant pour parent la "fenetre"
        self.bouton4 = QPushButton(self.trUtf8("Publish !"),self)
        self.bouton4.setFont(QFont("Comic Sans MS", 14,QFont.Bold,True))
        self.bouton4.setIcon(QIcon("../images/smile.png"))
        self.connect(self.bouton4, SIGNAL("clicked()"), self.liste3) 

        #Layout intermédiaire : boutons
        self.layoutH_boutons = QHBoxLayout()
        self.layoutH_boutons.addWidget(self.bouton3)
        self.layoutH_boutons.addWidget(self.bouton5)
        self.layoutH_boutons.addWidget(self.bouton4)
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
        self.layout_general.addLayout(self.layoutH_boutons)
        self.setLayout(self.layout_general)

    def liste3(self):
        
        # choix interaction
        if self.radio41.isChecked():
            self.choix_interaction = './electronBsub ' + self.choix_job + ' /afs/cern.ch/cms/utils/oval run ' + self.choix_etape + '.Val'
        if self.radio42.isChecked():
            self.choix_interaction = '/afs/cern.ch/cms/utils/oval run ' + self.choix_etape + '.Val'
        
        get_choix_calcul(self)        
        print "choix_calcul : ", self.choix_calcul
        
        # creation des repertoires
        cmd_folder_creation(self.choix_calcul)
        
        # if store is checked then copy of DQM*.root files
        if self.radio03.isChecked():
            copy_files(self)
        
        # get collections list to do (Pt35, Pt10, TTbar, .... if checked)
        coll_list = get_collection_list(self)

        # work to execute
        if self.radio04.isChecked():     # publish
            print "publish to be done"
            if self.radio13.isChecked(): # FAST
                print "Fast & publish"
                for val_Fast in ['VsFull', 'VsFast']:
                    for items in coll_list:
                        cmd = self.choix_interaction + self.choix_calcul + val_Fast + items + '_gedGsfE'
                        subprocess.call(cmd, shell = True)
            else:                        # no FAST
                print "no Fast & publish"
                for items in coll_list:
                    cmd = self.choix_interaction + self.choix_calcul + items + '_gedGsfE'
                    subprocess.call(cmd, shell = True)
            
            # rm dd*.olog dqm*.root 
            clean_files(self)
        else:
            print "no publish : general case"
            for items in coll_list:
                cmd = self.choix_interaction + self.choix_calcul + items + '_gedGsfE'
                subprocess.call(cmd, shell = True)

        print "fin"

    def liste4(self):
        print "liste 4"
        # mettre la fonction liste3 du ovalGui de Projet_DQM-V2
        list_search(self)
        to_transmit = [str(self.lineedit1.text()), str(self.lineedit3.text()), self.rel_list, self.ref_list]
        self.quelclient_update(to_transmit)
        
    def liste5(self):
        print "liste 5"
        # pour recuperer les fichiers DQM*.root
        print "liste 5 : coucou"
        if ( self.my_choice_rel ) :
            print "self.choice_rel : ", self.choice_rel
            if ( self.my_choice_ref ) :
                print "self.choice_ref : ", self.choice_ref 
                # step 1 : done
                option_is_from_data = "mc" # mc ou data
                option_mthreads = 3
                option_dry_run = False # False telecharge , True liste
                # step 2 : to be modified as a function
                part_rel_1 = self.choice_rel[0]
                part_rel_2 = self.choice_rel[1]
                itl2 = self.choice_rel[2]
                name_rel_base = "DQM_V0001_R000000001__RelVal" 
                name_rel_suffix = "__" + part_rel_1 + "-" + part_rel_2 + "__DQMIO.root"
                option_release_rel = str(part_rel_1) 
                for part_rel_3 in itl2:
                    name_rel = name_rel_base + part_rel_3 + name_rel_suffix
                    print "name_rel : ", name_rel
                    option_regexp_rel = str( name_rel ) 
                    cmd_fetch(option_is_from_data, option_release_rel, option_regexp_rel, option_mthreads, option_dry_run)
                part_ref_1 = self.choice_ref[0]
                part_ref_2 = self.choice_ref[1]
                itf2 = self.choice_ref[2]
                name_ref_base = "DQM_V0001_R000000001__RelVal" 
                name_ref_suffix = "__" + part_ref_1 + "-" + part_ref_2 + "__DQMIO.root"
                option_release_ref = str(part_ref_1) 
                for part_ref_3 in itf2:
                    name_ref = name_ref_base + part_ref_3 + name_ref_suffix
                    print "name_ref : ", name_ref
                    option_regexp_ref = str( name_ref ) 
                    cmd_fetch(option_is_from_data, option_release_ref, option_regexp_ref, option_mthreads, option_dry_run)
                # step 2 : done
                # step 3 : done

            else:
                print "no reference choosed. Nothing to do."
        else:
            print "no release choosed. Nothing to do."

        # step 1 : si pas de release et/ou de reference : ne rien faire
        # step 2 : refaire une liste des fichiers a recuperer
        # step 3 : charger les fichiers (on passe le nom du fichier comme option -e="nom_fichier")
        # (liste_fichiers_3) = cmd_fetch(option_is_from_data, option_release_3, option_regexp, option_mthreads, option_dry_run)
         
    def quelclient_update(self, to_transmit):
        from operator import itemgetter
        """Lance la deuxième fenêtre"""
        self.quelclient = Quelclient()
        
        self.rel_list_mod = []
        self.ref_list_mod = []
        self.rel_list_mod2 = []
        self.ref_list_mod2 = []
        self.my_choice_rel = "" # for transmission data between the 2 windows
        self.my_choice_ref = "" # for transmission data between the 2 windows
    
        self.quelclient.bouton.setText("Quit") # to be removed ?
        self.quelclient.TextEdit_H1.clear()
        self.quelclient.TextEdit_H2.clear()
        self.quelclient.QGBox_H1.setTitle(to_transmit[0])
        self.quelclient.QGBox_H2.setTitle(to_transmit[1])
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
        
#        for items in self.rel_list_mod:
#            print items
#        for items in self.ref_list_mod:
#            print items

        # to be removed later
        for items in self.rel_list_mod:
            line_TE = ''
            for items2 in items:
                line_TE += items2 + ' '
            self.quelclient.TextEdit_H1.append(line_TE)
        for items in self.ref_list_mod:
            line_TE = ''
            for items2 in items:
                line_TE += items2 + ' '
            self.quelclient.TextEdit_H2.append(line_TE)
        # to be removed later
        
        print "tablo avant : ", self.rel_list_mod
        self.rel_list_mod2 = list_simplify(self.rel_list_mod)
        print "retour tablo : ", self.rel_list_mod2
#        print "tablo avant : ", self.ref_list_mod
        self.ref_list_mod2 = list_simplify(self.ref_list_mod)
#        print "retour tablo : ", self.ref_list_mod2

        i = 0
        k = 0
        self.buttons_rel = []
        for items in self.rel_list_mod2:
            it1 = ''
            it2 = items[2]
            for it in it2:
                print "+-+-+-", it
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
                self.quelclient.gbox_H1.addWidget(self.buttons_rel[i], k, j)
                self.connect(self.buttons_rel[i], SIGNAL("clicked()"), self.buttons_relClicked)
                j += 1
                i += 1
            k += 1           
#        self.buttons_rel[1].setChecked(True) # default
            
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
                self.quelclient.gbox_H2.addWidget(self.buttons_ref[i], k, j)
                self.connect(self.buttons_ref[i], SIGNAL("clicked()"), self.buttons_refClicked)
                j += 1
                i += 1
            k += 1           
#        self.buttons_ref[1].setChecked(True) # default
            
        # en cas de signal "fermeturequelclient()" reçu de self.quelclient => exécutera clienchoisi 
        self.connect(self.quelclient, SIGNAL("fermeturequelclient(PyQt_PyObject)"), self.clientchoisi) 
        # la deuxième fenêtre sera 'modale' (la première fenêtre sera inactive)
        self.quelclient.setWindowModality(QtCore.Qt.ApplicationModal)
        # appel de la deuxième fenêtre
        self.quelclient.show()

    def clientchoisi(self, x):
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
                        print self.buttons_rel[i].text(), " checked with (%i, %i, %i)", i, j, k
                        print self.buttons_rel[i].text(), " checked with ", self.rel_list_mod2[k]
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
                        print self.buttons_ref[i].text(), " checked with (%s, %s, %s)", i, j, k
                        print self.buttons_ref[i].text(), " checked with ", self.ref_list_mod2[k]
                j += 1
                i += 1
            k += 1
        QtCore.QCoreApplication.processEvents()
                
    def radio01Clicked(self):
        if self.radio01.isChecked():
            self.QGBox2.setEnabled(False)
            self.QGBox2.setVisible(False)
#            self.label62.setVisible(False) # new
#            self.lineedit3.setVisible(False) # new
            self.choix_etape = 'analyze' # default
            self.choix_calcul = 'Full'
        QtCore.QCoreApplication.processEvents()

    def radio02Clicked(self):
        if self.radio02.isChecked():
            self.QGBox2.setEnabled(False)
            self.QGBox2.setVisible(False)
#            self.label62.setVisible(False) # new
#            self.lineedit3.setVisible(False) # new
            self.choix_etape = 'finalize' # default
            self.choix_calcul = 'Full'
        QtCore.QCoreApplication.processEvents()
        
    def radio03Clicked(self):
        if self.radio03.isChecked():
            self.QGBox2.setEnabled(True)
            self.QGBox2.setVisible(True)
#            self.label62.setVisible(False) # new
#            self.lineedit3.setVisible(False) # new
            self.choix_etape = 'store' # default
            self.choix_calcul = 'Full'
        QtCore.QCoreApplication.processEvents()

    def radio04Clicked(self):
        if self.radio04.isChecked():
            self.QGBox2.setEnabled(False)
            self.QGBox2.setVisible(False)
#            self.label62.setVisible(True) # new
#            self.lineedit3.setVisible(True) # new
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

    def checkAllNone1Clicked(self):
        if self.checkAllNone1.isChecked():
            print "All"
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
            print "None"
            self.check31.setChecked(False)
            self.check32.setChecked(False)
            self.check33.setChecked(False)
            self.check34.setChecked(False)
            self.check35.setChecked(False)
            self.check36.setChecked(False)
            self.check37.setChecked(False)
            self.check38.setChecked(False)
        QtCore.QCoreApplication.processEvents() 
        