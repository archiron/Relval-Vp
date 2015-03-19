#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys,subprocess
import urllib2
import re
from getEnv import env

def liste(): # execute la cmd pwd.
    import subprocess
    cmsenv = env()

    chemin = []
    proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    chemin = out.split('\n')
    return chemin
    
def cmd_test():
    # fct test retourne 2 nb
    cmsenv = env()
    print "fichiers txt pour la release : ", cmsenv.CMSSWBASECMSSWVERSION
    toto = "fichiers txt pour la release : "
    titi = cmsenv.CMSSWBASECMSSWVERSION
    print toto, titi
    return toto, titi

def cmd_folder_creation(choix_calcul):
    import subprocess, os
    if ( ( choix_calcul == 'Full' ) or ( choix_calcul == 'gedvsgedFull'  )):
        if not os.path.exists("GED1"):
            print "Creation of GED folder"
            os.makedirs("GED1")
        else:
            print "GED folder already created"
    elif ( choix_calcul == 'Fast' ):
        if not os.path.exists("FAST1"):
            print "Creation of FAST folder"
            os.makedirs("FAST1")
        else:
            print "FAST folder already created"
    elif ( choix_calcul == 'PileUp' ):
        if not os.path.exists("PU251"):
            print "Creation of PU251 folder"
            os.makedirs("PU251")
        else:
            print "PU251 folder already created"
        if not os.path.exists("PU501"):
            print "Creation of PU501 folder"
            os.makedirs("PU501")
        else:
            print "PU501 folder already created"
        
    return 
    
def get_collection_list(self):
    import subprocess, os
    collection_list = []
    if self.radio11.isChecked(): # FULL
        if self.check31.isChecked():
            collection_list.append('Pt10Startup_UP15')
        if self.check32.isChecked():
            collection_list.append('Pt35Startup_UP15')
        if self.check33.isChecked():
            collection_list.append('Pt1000Startup_UP15')
        if self.check34.isChecked():
            collection_list.append('QcdPt80Pt120Startup_13')
        if self.check35.isChecked():
            collection_list.append('TTbarStartup_13')
        if self.check36.isChecked():
            collection_list.append('ZEEStartup_13')
    else: #FAST, PU
        if self.check37.isChecked():
            collection_list.append('TTbarStartup')
        if self.check38.isChecked():
            collection_list.append('ZEEStartup')
    return collection_list

def get_choix_calcul(self):
    if self.radio11.isChecked(): # FULL
        self.choix_calcul = 'Full'
        if self.radio04.isChecked():
            self.choix_calcul = 'gedvsgedFull'
    if self.radio12.isChecked(): # PU
        self.choix_calcul = 'PileUp'
    if self.radio13.isChecked(): # FAST
        self.choix_calcul = 'Fast'
    return
    
def clean_files(self):
    import os,sys,subprocess,glob
#    print glob.glob('dd*.olog')
#    print glob.glob('dqm*.root')
    for items in glob.glob('dd*.olog'): 
        os.remove(items)
    for items in glob.glob('dqm*.root'): 
        os.remove(items)
#    print glob.glob('dd*.olog')
#    print glob.glob('dqm*.root')
    return
    
def copy_files(self):
    import os,sys,subprocess,glob,re,shutil
    for items in glob.glob('DQM*.root'): 
        pref1,pref2,chaine,exten = items.split("__")
        new_name = 'electronHistos.' + chaine + '.root'
        shutil.copyfile(items, new_name)
    return