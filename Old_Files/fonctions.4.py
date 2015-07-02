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
     
def cmd_eos(choix_gedGsf, choix_simus, choix_reco):
# choix_gedGsf : Gsf or gedGsf choice (default : gedGsf)
# choix_simus : Gsf or gedGsf choice (default : gedGsf)
# choix_reco : RECO (root) files or DQM files (default : RECO)
    import subprocess
    cmsenv = env()
#    print choix_simus
    (av1, ap1) = choix_gedGsf.split(' : ')
    choix_gedGsf = ap1
    (av2, ap2) = choix_simus.split(' : ')
    choix_simus = ap2
    (av1, ap1) = choix_reco.split(' : ')
    if ap1 != 'DQM':
        choix_reco = 'RECO'
        liste_reco = ['GEN-SIM-RECO', 'GEN-SIM-DIGI-RECO']
        if choix_simus == 'Fast':
            liste_reco = ['GEN-SIM-DIGI-RECO']
    else :
        # ATTENTION DQM ou DQMIO
        choix_reco = 'DQMIO'
        liste_reco = ['DQMIO']
	
    list_cmdes_eos = []
    list_cmdes_eos_tmp = []
    print "methode par", cmsenv.eosText()
    for type in liste_reco: # liste par DQM ou GEN-SIM-RECO, GEN-SIM-DIGI-RECO
        list_cmdes_eos.append("\n===========") 
        list_cmdes_eos.append(type) # ajoute type a la liste des elements 
        list_cmdes_eos.append("===========") 
        print "==========="
        print "++", type, "++"
        print "==========="
        liste_coll = cmsenv.liste_ged()
        if choix_gedGsf != 'gedGsf':
            liste_coll = cmsenv.liste_Gsf()
        for name in liste_coll: # liste par TTbar, ZEE, SingleElectronPtXX, ...
            print "++", name, " :"
            print "----------"
            a = cmsenv.eosText() + '/' + name + '/' + type
            proc = subprocess.Popen([a], stdout=subprocess.PIPE, shell=True) # séparer la commande des arguments
            (out, err) = proc.communicate()
            if out != '': 
                list_cmdes_eos.append("\n" + name) # ajoute name a la liste des elements 
                list_cmdes_eos.append("----------") 
                list_cmdes_eos_tmp = out.split('\n')
                #print list_cmdes_eos_tmp
                for elem in list_cmdes_eos_tmp:
                    print elem		
                    list_cmdes_eos.append(elem)	
    return list_cmdes_eos

def cmd_relval(choix_gedGsf, choix_reco):
    # liste les fichiers txt du site http://cms-project-relval.web.cern.ch/cms-project-relval/relval_stats/
    # choix_gedGsf : Gsf or gedGsf choice (default : gedGsf)
    # choix_simus : Gsf or gedGsf choice (default : gedGsf)
    # choix_reco : RECO (root) files or DQM files (default : RECO)
    cmsenv = env()
    print "fichiers txt pour la release : ", cmsenv.CMSSWBASECMSSWVERSION
    print "autre methode par", cmsenv.eosFind()
    base = '<img src="/icons/text.gif" alt="[TXT]">' #pas beau, a revoir
    liste_fichiers = (urllib2.urlopen(cmsenv.eosFind()).read()).split('\n')
    print choix_reco
    (av2, ap2) = choix_gedGsf.split(' : ')
    choix_gedGsf = ap2
    (av1, ap1) = choix_reco.split(' : ')
    if ap1 != 'DQM':
        choix_reco = 'RECO'
        liste_reco = ['GEN-SIM-RECO', 'GEN-SIM-DIGI-RECO']
    else :
        choix_reco = 'DQM'
        liste_reco = ['DQM']

    j = 0
    list_fichiers_txt = []
    list_elements_txt = []
    for elem in liste_fichiers:
    	if re.search(cmsenv.CMSSWBASECMSSWVERSION, elem): # cherche si la release est dans le nom du fichier
        #if re.search('CMSSW_7_0_0_pre', elem):
            j += 1
            fichier_false = False
            elem = elem.replace(base, '') #pas beau, a revoir
            pos1 = elem.find('href=') 
            pos2 = elem.find('>') 
            fileName = elem[pos1+6:pos2-1]
            fichier = cmsenv.eosFind() + fileName # adresse web du fichier
            print "fichier : ", fichier
            liste_glob = (urllib2.urlopen(fichier).read()).split('\n') # liste globale de ts les elements du fichier
            for elems in liste_glob:
                for type in liste_reco:
                    if re.search(type, elems):
                        liste_coll = cmsenv.liste_ged()
                        if choix_gedGsf != 'gedGsf':
                            liste_coll = cmsenv.liste_Gsf()
                        for item2 in liste_coll: # liste par TTbar, ZEE, SingleElectronPtXX, ... 
                            if re.search(item2 + '/', elems):
                                chaine = cmsenv.CMSSWBASECMSSWVERSION + '-' # cherche des chaines comme CMSSW_7_0_0_pre4- et pas CMSSW_7_0_0_pre4_GEANT10-
                                if re.search(chaine, elems):
                                    print "--- OK", elems, " :: ", item2 #, " :: ", item
                                    fichier_false = True
                                    list_elements_txt.append(elems) # ajoute a la liste des elements 
                                if fichier_false:
                                    list_fichiers_txt.append(fileName) # ajoute a la liste des fichiers presentant CMSSWBASECMSSWVERSION dans leur titre
    print "il y a %s fichiers" % j
	
    return list_fichiers_txt, list_elements_txt

def cmd_listeRECO():
    import subprocess
    cmsenv = env()
    liste_fichiersRECO = []
    print "liste RECO"
    print "methode par", cmsenv.eosStore()
    liste_temp = (urllib2.urlopen(cmsenv.eosStore()).read()).split('\n')
    i = 0
    for j in range(9):
#        print liste_temp[0]
        liste_temp.pop(0)
    for j in range(5):
        liste_temp.pop()
    for elem in liste_temp:
        pos1 = elem.find('href="') 
        pos2 = elem.find('/">') 
        fileName = elem[pos1+6:pos2-0]
        i += 1
        print "fichier ", i, " : ", fileName
        liste_fichiersRECO.append(fileName)	

    return liste_fichiersRECO

def cmd_listeDQM():
    import subprocess
    cmsenv = env()
    liste_fichiersDQM = []
    print "liste DQM"
    print "methode par", cmsenv.eosFind()
    base = '<img src="/icons/text.gif" alt="[TXT]">' #pas beau, a revoir
    liste_temp = (urllib2.urlopen(cmsenv.eosFind()).read()).split('\n')
    i = 0
    for elem in liste_temp:
        elem = elem.replace(base, '') #pas beau, a revoir
        pos1 = elem.find('href="') 
        pos2 = elem.find('">') 
        fileName = elem[pos1+6:pos2-4]
    	if re.search("CMSSW_", fileName): # cherche si le fichier commence par CMSSW_
            if fileName != '':
                i += 1
#                fileName = fileName.replace('.txt', '')
                print "fichier ", i, " : ", fileName
                liste_fichiersDQM.append(fileName)	
    
    return liste_fichiersDQM

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

def get_collection_list_search(self):
    import subprocess, os
    collection_list = []
    if self.radio11.isChecked(): # FULL 
        if self.check31.isChecked():
            collection_list.append('RelValSingleElectronPt10_UP15')
        if self.check32.isChecked():
            collection_list.append('RelValSingleElectronPt35_UP15')
        if self.check33.isChecked():
            collection_list.append('RelValSingleElectronPt1000_UP15')
        if self.check34.isChecked():
            collection_list.append('RelValQCD_Pt_80_120_13')
        if self.check35.isChecked():
            collection_list.append('RelValTTbar_13')
        if self.check36.isChecked():
            collection_list.append('RelValZEE_13')
    else: #FAST, PU
        if self.check37.isChecked():
            collection_list.append('TTbar_13')
        if self.check38.isChecked():
            collection_list.append('ZEE_13')
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
    
def get_choix_calcul_search(self):
    if self.radio11.isChecked(): # FULL
        get_choix_calcul = 'Full'
    if self.radio12.isChecked(): # PU
        get_choix_calcul = 'PU'
    if self.radio13.isChecked(): # FAST
        get_choix_calcul = 'Fast'
    return get_choix_calcul
    
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
    
def auth_wget2(url, chunk_size=1048576):
    from os.path import basename, isfile
    from optparse import OptionParser
    from urllib2 import build_opener, Request
    """Returns the content of specified URL, which requires authentication.
    If the content is bigger than 1MB, then save it to file.
    """
    try:
        from Utilities.RelMon.authentication import X509CertOpen
    except ImportError:
        from authentication import X509CertOpen

    opener = build_opener(X509CertOpen())
    url_file = opener.open(Request(url))
    size = int(url_file.headers["Content-Length"])

    if size < 1048576:   # if File size < 1MB
        filename = basename(url)    #still download
        readed = url_file.read()    ## and then check if its not an empty dir (parent directory)
        if filename != '':
            outfile = open(filename, 'wb')  #then write File to local system
            outfile.write(readed)
        return readed

    filename = basename(url)

    if isfile("./%s" % filename):
        print '%s. Exists on disk. Skipping.' % (filename)
        return

    print ' Downloading... %s' % (filename)
    file = open(filename, 'wb')
    chunk = url_file.read(chunk_size)
    while chunk:
        file.write(chunk)
        chunk = url_file.read(chunk_size)
    print '%s.  Done.' % (filename)
    file.close()

def cmd_fetch(option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run):
    # fetchall_from_DQM_v2.py -r CMSSW_7_0_0 -e='TTbar,PU,25' --mc --dry
    import re
    import sys
    import os

    from multiprocessing import Pool, Queue, Process
    from Queue import Empty
    from os.path import basename, isfile
    from optparse import OptionParser
    from urllib2 import build_opener, Request
    
    print "CMD_FETCH : "
    cmsenv = env()
   
    ## Define options
#    option_is_from_data = "mc" # mc ou data
#    option_release = cmsenv.getCMSSWBASECMSSWVERSION()
#    option_regexp = 'TTbar,PU,25'
#    option_mthreads = 3
#    option_dry_run = True
    print option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run
        
    try:
        from Utilities.RelMon.authentication import X509CertOpen
    except ImportError:
        from authentication import X509CertOpen

    def auth_wget(url, chunk_size=1048576):
        """Returns the content of specified URL, which requires authentication.
        If the content is bigger than 1MB, then save it to file.
        """
        opener = build_opener(X509CertOpen())
        url_file = opener.open(Request(url))
        size = int(url_file.headers["Content-Length"])

        if size < 1048576:   # if File size < 1MB
            filename = basename(url)    #still download
            readed = url_file.read()    ## and then check if its not an empty dir (parent directory)
            if filename != '':
                outfile = open(filename, 'wb')  #then write File to local system
                outfile.write(readed)
            return readed

        filename = basename(url)
        file_id = selected_files.index(filename)

        if isfile("./%s" % filename):
            print '%d. Exsits on disk. Skipping.' % (file_id +1)
            return

        print '%d. Downloading...' % (file_id +1)
        file = open(filename, 'wb')
        # progress = 0
        chunk = url_file.read(chunk_size)
        while chunk:
            file.write(chunk)
            # progress += chunk_size
            chunk = url_file.read(chunk_size)
        print '%d.  Done.' % (file_id +1)
        file.close()

    ## Use options
    relvaldir = "RelVal"
    if option_is_from_data == 'data':
        relvaldir = "RelValData"
    print "relvaldir : ", relvaldir
    release = re.findall('(CMSSW_\d*_\d*_)\d*(?:_[\w\d]*)?', option_release)
    print release
    if not release:
        parser.error('No such CMSSW release found. Please check the ``--release`` commandline option value.')
    releasedir = release[0] + "x"
    print "releasedir : ", releasedir
    base_url = 'https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/'
    filedir_url = base_url + relvaldir + '/' + releasedir + '/'
    filedir_html = auth_wget(filedir_url)

    #auth_wget("https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/Run2012/JetHT/0002029xx/DQM_V0001_R000202950__JetHT__Run2012C-PromptReco-v2__DQM.root")
    #auth_wget("https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/RelValData/CMSSW_5_3_x/DQM_V0001_R000205921__JetHT__CMSSW_5_3_3_patch1-PR_newconditions_RelVal_R205921_121105-v2__DQM.root")

    file_list_re = re.compile(r"<a href='[-./\w]*'>([-./\w]*)<")
    all_files = file_list_re.findall(filedir_html)[1:]  # list of file names

    ### Fetch the files, using multi-processing
    file_res = [re.compile(r) for r in option_regexp.split(',') + [option_release]]
    selected_files = [f for f in all_files if all([r.search(f) for r in file_res])]

    print 'Downloading files:'
    for i, name in enumerate(selected_files):
        print '%d. %s' % (i+1, name)
        
    if option_dry_run:
        return selected_files
    if not option_dry_run:
        print '\nProgress:'
        pool = Pool(option_mthreads)
        pool.map(auth_wget2, [filedir_url + name for name in selected_files])
    
    return 

def clean_collections(collection, gccs):
    import re
    i = 0
    temp = []
    for items in collection:
#        print "data ", i, " : ", items
        i += 1
        if ( gccs == 'Full' ):
            if ( re.search('PU', items) ):
                print " PU exist in Full", items # to be removed
            elif ( re.search('Fast', items) ):
                print " Fast exist in Full", items # to be removed
            else:
                temp.append(items)
        elif ( gccs == 'PU' ):
            if ( re.search('Fast', items) ):
                print " Fast exist in PU", items # to be removed
            else:
                temp.append(items)
        else:
            if ( re.search('PU', items) ):
                print " PU exist in Fast", items # to be removed
            else:
                temp.append(items)
    return temp

def list_search(self):
    texte_release1 = self.lineedit1.text()
    texte_release3 = self.lineedit3.text()
    print "texte 1 : ", texte_release1
    print "texte 3 : ", texte_release3
        
    # on fera la fonction par un appel a cmd_fetchall(options)
    # ou options regroupera option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run
        
    ## Define options
    option_is_from_data = "mc" # mc ou data
    option_release_1 = str(self.lineedit1.text()) # self.cmsenv.getCMSSWBASECMSSWVERSION()
    option_release_3 = str(self.lineedit3.text()) # self.cmsenv.getCMSSWBASECMSSWVERSION()
    option_regexp = '_RelValTTbar_13' # str( self.lineedit4.text() ) to be removed
    option_mthreads = 3
    option_dry_run = True # False for loading files
    self.gccs = get_choix_calcul_search(self) 
    print "**********", "choix calcul : ", self.choix_calcul, self.gccs # to be removed
    
    # get collections list to do (Pt35, Pt10, TTbar, .... if checked)
    coll_list = get_collection_list_search(self)
    
    self.rel_list = []
    self.ref_list = []
    
    for items in coll_list:
#        print items
        option_regexp = str( items )
        if ( self.gccs != 'Full' ):
            option_regexp += ',' + str(self.gccs)
        print "**********", items, "- ", option_release_1 # to be removed
        (liste_fichiers_1) = cmd_fetch(option_is_from_data, option_release_1, option_regexp, option_mthreads, option_dry_run)
        self.rel_list += liste_fichiers_1
        print "**********", items, "- ", option_release_3 # to be removed
        (liste_fichiers_3) = cmd_fetch(option_is_from_data, option_release_3, option_regexp, option_mthreads, option_dry_run)
        self.ref_list += liste_fichiers_3
        
    print "\n****** cleaning ******"
    self.rel_list = clean_collections(self.rel_list, self.gccs)
    self.ref_list = clean_collections(self.ref_list, self.gccs)
    print "****** done ******"
    
    # si on veut comparer deux releases par fichiers DQM
    # self.listeReference.currentText() pour la reference
    #print "reference : ", self.listeReference.currentText() # reste à extraire la release de reference
    #option_release = 'CMSSW_7_2_0_pre4' # self.listeReference.currentText()    
    #cmd_fetch(option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run)

    #affichage des fichiers (n'affiche que la derniere recherche)
    print '\n-----'
    for items in self.rel_list:
        print items
        print explode_item(items)
    print '-----'
    for items in self.ref_list:
        print items

    return 

def explode_item(item):
    # initial file name : DQM_V0001_R000000001__RelValTTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1__DQMIO.root
    # prefix in DQM_V0001_R000000001__ removed : RelValTTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1__DQMIO.root
    # suffix in __DQMIO.root removed : RelVal
    # new prefix in RelVal removed : TTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1
    # splitting with __ : TTbar_13 CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1
    # splitting second term with - : TTbar_13 CMSSW_7_4_0_pre8 PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1
    
    temp_item = item[22:] # DQM_V0001_R000000001__ removed
    temp_item = temp_item[:-12] # __DQMIO.root removed
    temp_item = temp_item[6:] # RelVal removed
    temp_item = temp_item.split('__')
#    print "coucou : ", temp_item
    temp_item2 = temp_item[1].split('-', 1)
    temp_item = [ temp_item[0] ]
    for it in temp_item2:
        temp_item.append(it)
#    print "coucou : ", temp_item
    return temp_item
    