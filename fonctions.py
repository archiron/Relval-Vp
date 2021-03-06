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
#    print "methode par", cmsenv.eosText()
    for type in liste_reco: # liste par DQM ou GEN-SIM-RECO, GEN-SIM-DIGI-RECO
        list_cmdes_eos.append("\n===========") 
        list_cmdes_eos.append(type) # ajoute type a la liste des elements 
        list_cmdes_eos.append("===========") 
#        print "==========="
#        print "++", type, "++"
#        print "==========="
        liste_coll = cmsenv.liste_ged()
        if choix_gedGsf != 'gedGsf':
            liste_coll = cmsenv.liste_Gsf()
        for name in liste_coll: # liste par TTbar, ZEE, SingleElectronPtXX, ...
#            print "++", name, " :"
#            print "----------"
            a = cmsenv.eosText() + '/' + name + '/' + type
            proc = subprocess.Popen([a], stdout=subprocess.PIPE, shell=True) # séparer la commande des arguments
            (out, err) = proc.communicate()
            if out != '': 
                list_cmdes_eos.append("\n" + name) # ajoute name a la liste des elements 
                list_cmdes_eos.append("----------") 
                list_cmdes_eos_tmp = out.split('\n')
                #print list_cmdes_eos_tmp
                for elem in list_cmdes_eos_tmp:
#                    print elem		
                    list_cmdes_eos.append(elem)	
    return list_cmdes_eos

def cmd_relval(choix_gedGsf, choix_reco):
    # liste les fichiers txt du site http://cms-project-relval.web.cern.ch/cms-project-relval/relval_stats/
    # choix_gedGsf : Gsf or gedGsf choice (default : gedGsf)
    # choix_simus : Gsf or gedGsf choice (default : gedGsf)
    # choix_reco : RECO (root) files or DQM files (default : RECO)
    cmsenv = env()
#    print "fichiers txt pour la release : ", cmsenv.CMSSWBASECMSSWVERSION
#    print "autre methode par", cmsenv.eosFind()
    base = '<img src="/icons/text.gif" alt="[TXT]">' #pas beau, a revoir
    liste_fichiers = (urllib2.urlopen(cmsenv.eosFind()).read()).split('\n')
#    print choix_reco
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
#            print "fichier : ", fichier
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
#                                    print "--- OK", elems, " :: ", item2 #, " :: ", item
                                    fichier_false = True
                                    list_elements_txt.append(elems) # ajoute a la liste des elements 
                                if fichier_false:
                                    list_fichiers_txt.append(fileName) # ajoute a la liste des fichiers presentant CMSSWBASECMSSWVERSION dans leur titre
#    print "il y a %s fichiers" % j
	
    return list_fichiers_txt, list_elements_txt

def cmd_listeRECO():
    import subprocess
    cmsenv = env()
    liste_fichiersRECO = []
#    print "liste RECO"
#    print "methode par", cmsenv.eosStore()
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
#        print "fichier ", i, " : ", fileName
        liste_fichiersRECO.append(fileName)	

    return liste_fichiersRECO

def cmd_listeDQM():
    import subprocess
    cmsenv = env()
    liste_fichiersDQM = []
#    print "liste DQM"
#    print "methode par", cmsenv.eosFind()
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
#                print "fichier ", i, " : ", fileName
                liste_fichiersDQM.append(fileName)	
    
    return liste_fichiersDQM

def cmd_test():
    # fct test retourne 2 nb
    cmsenv = env()
#    print "fichiers txt pour la release : ", cmsenv.CMSSWBASECMSSWVERSION
    toto = "fichiers txt pour la release : "
    titi = cmsenv.CMSSWBASECMSSWVERSION

def cmd_folder_creation(choix_calcul, working_dir):
    import subprocess, os, datetime
    now = datetime.datetime.now()
    newDirName = now.strftime("%Y_%m_%d-%H%M%S")
#    print "Making directory " + newDirName
#    print "working dir : ", working_dir
    actual_dir = os.getcwd()
#    print "cmd_folder_creation - actual dir : ", actual_dir
    os.chdir(working_dir)
#    print "cmd_folder_creation - je suis en : ", os.getcwd()
    if ( ( choix_calcul == 'Full' ) or ( choix_calcul == 'gedvsgedFull'  )):
        newDirName = '/GED_' + newDirName
    elif ( choix_calcul == 'Fast' ):
        newDirName = '/FAST_' + newDirName
    elif ( choix_calcul == 'PileUp' ):
        newDirName = '/PU_' + newDirName
    
    m_dir = working_dir + newDirName
    os.makedirs(m_dir)
    tmp = m_dir
    
    os.chdir(actual_dir)
    return tmp

def cmd_working_dirs_creation(self):
#    print "cmd_working_dirs_creation"
    self.working_dir_rel = self.working_dir_base + '/' + str(self.lineedit1.text()[6:])
    self.working_dir_ref = self.working_dir_rel + '/' + str(self.lineedit3.text()[6:])
    return
    
def get_collection_list(self):
    import subprocess, os
    collection_list = []
    if self.radio11.isChecked(): # FULL
        if self.check31.isChecked():
            collection_list.append('Pt10Startup') #_UP15
        if self.check32.isChecked():
            collection_list.append('Pt35Startup') #_UP15
        if self.check33.isChecked():
            collection_list.append('Pt1000Startup') #_UP15
        if self.check34.isChecked():
            collection_list.append('QcdPt80120Startup') #_13 QcdPt80Pt120Startup_13
        if self.check35.isChecked():
            collection_list.append('TTbarStartup_13') #
        if self.check36.isChecked():
            collection_list.append('ZEEStartup_13') #
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
            collection_list.append('RelValSingleElectronPt10') #_UP15
        if self.check32.isChecked():
            collection_list.append('RelValSingleElectronPt35') #_UP15
        if self.check33.isChecked():
            collection_list.append('RelValSingleElectronPt1000') #_UP15
        if self.check34.isChecked():
            collection_list.append('RelValQCD_Pt_80_120') #_13
        if self.check35.isChecked():
            collection_list.append('RelValTTbar_13') #
        if self.check36.isChecked():
            collection_list.append('RelValZEE_13') #
    else: #FAST, PU
        if self.check37.isChecked():
            collection_list.append('TTbar_13')
        if self.check38.isChecked():
            collection_list.append('ZEE_13')
    return collection_list
   
def get_choix_calcul(self):
    if self.radio11.isChecked(): # FULL
        self.choix_calcul = 'Full'
        self.choix_calcul = 'gedvsgedFull' # because radio04 is always checked
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
    import os,sys,subprocess,glob,shutil
#    print 'folder : ', self.folder_name
    for items in glob.glob('dd*.olog'): 
        os.remove(items)
    for items in glob.glob('dqm*.root'): 
        os.remove(items)
    for items in glob.glob(self.working_dir_base + '/*.olog'): 
        shutil.move(items, self.folder_name)
#    for items in glob.glob('*.root'): 
#        shutil.copy(items, self.folder_name)
#        shutil.move(items, self.folder_name)
    shutil.copy('OvalFile', self.folder_name)
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
    
#    print "\n CMD_FETCH : "
    cmsenv = env()
   
    ## Define options
#    option_is_from_data = "mc" # mc ou data
#    option_release = cmsenv.getCMSSWBASECMSSWVERSION()
#    option_regexp = 'TTbar,PU,25'
#    option_mthreads = 3
#    option_dry_run = True
#    print option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run
        
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
        print "size= ", size

        #if size < 1048576:   # if File size < 1MB
        if size < 2048576:   # if File size < 2MB
            filename = basename(url)    #still download
            readed = url_file.read()    ## and then check if its not an empty dir (parent directory)
            if filename != '':
                outfile = open(filename, 'wb')  #then write File to local system
                outfile.write(readed)
            return readed

        filename = basename(url)
        file_id = selected_files.index(filename)

        if isfile("./%s" % filename):
            print '%d. Exists on disk. Skipping.' % (file_id +1)
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
    release = re.findall('(CMSSW_\d*_\d*_)\d*(?:_[\w\d]*)?', option_release)
    if not release:
        parser.error('No such CMSSW release found. Please check the ``--release`` commandline option value.')
    releasedir = release[0] + "x"
    base_url = 'https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/'
#    base_url = 'https://cmsweb.cern.ch/dqm/relval-test/data/browse/ROOT/'
    filedir_url = base_url + relvaldir + '/' + releasedir + '/'
#    filedir_url = 'http://cms-project-relval.web.cern.ch/cms-project-relval/relval_stats/'
    print "AAAAAAA : ", filedir_url
    filedir_html = auth_wget(filedir_url)

    #auth_wget("https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/Run2012/JetHT/0002029xx/DQM_V0001_R000202950__JetHT__Run2012C-PromptReco-v2__DQM.root")
    #auth_wget("https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/RelValData/CMSSW_5_3_x/DQM_V0001_R000205921__JetHT__CMSSW_5_3_3_patch1-PR_newconditions_RelVal_R205921_121105-v2__DQM.root")

    file_list_re = re.compile(r"<a href='[-./\w]*'>([-./\w]*)<")
    all_files = file_list_re.findall(filedir_html)[1:]  # list of file names
#    print "cmd_fetch : ", all_files

    ### Fetch the files, using multi-processing
    print "cmd_fetch : ", option_regexp.split(',') + [option_release]
    file_res = [re.compile(r) for r in option_regexp.split(',') + [option_release]]

    selected_files = [f for f in all_files if all([r.search(f) for r in file_res])]
#    print selected_files

    print 'Downloading files:'
    for i, name in enumerate(selected_files):
        print '%d. %s' % (i+1, name)
        
    if option_dry_run:
        print "done"
        return selected_files
    if not option_dry_run:
        print '\nProgress:'
        pool = Pool(option_mthreads)
        pool.map(auth_wget2, [filedir_url + name for name in selected_files])
    
    return 

def clean_collections(self, collection, gccs):
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
#                temp.append(items) # TEMP. To be removed
            else:
                if self.checkRECOMiniAOD3.isChecked(): # pmx
#                    if ( re.search('PUpmx', items) ):
#                        temp.append(items)
                    temp.append(items)
                else: # no pmx, only PU
                    if ( not re.search('pmx', items) ):
                        temp.append(items)
#                temp.append(items)
        else: # gccs == 'FAST'
            if ( re.search('PU', items) ):
                print " PU exist in Fast", items # to be removed
            else:
                temp.append(items)
    return temp

def list_search(self):
    # on fera la fonction par un appel a cmd_fetchall(options)
    # ou options regroupera option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run
        
    ## Define options
    option_is_from_data = "mc" # mc ou data
    option_release_1 = str(self.lineedit1.text()) # self.cmsenv.getCMSSWBASECMSSWVERSION()
    option_release_3 = str(self.lineedit3.text()) # self.cmsenv.getCMSSWBASECMSSWVERSION()
    if self.checkRECOMiniAOD2.isChecked(): # miniAOD
        option_release_3 = option_release_1
    if self.checkRECOMiniAOD3.isChecked(): # pmx
        option_release_3 = option_release_1
    option_regexp = '_RelValTTbar_13' # str( self.lineedit4.text() ) to be removed
    option_mthreads = 3
    option_dry_run = True # False for loading files
    self.gccs = get_choix_calcul_search(self) 
#    print "**********", "choix calcul : ", self.choix_calcul, self.gccs # to be removed
    
    # get collections list to do (Pt35, Pt10, TTbar, .... if checked)
    coll_list = get_collection_list_search(self)
    
    self.rel_list = []
    self.ref_list = []
    
    for items in coll_list:
        print "ITEMS : ", items
        option_regexp = str( items ) + '__'
#        if ( self.gccs != 'Full' ):
#            option_regexp += ',' + str(self.gccs)
        if ( self.gccs == 'Fast' ):
            option_regexp += ',' + str(self.gccs)
        if ( self.gccs == 'PU' ):
            option_regexp += ',PU'
#        print "**********", items, "- ", option_release_3 # to be removed
        (liste_fichiers_3) = cmd_fetch(option_is_from_data, option_release_3, option_regexp, option_mthreads, option_dry_run)
        self.ref_list += liste_fichiers_3

        option_regexp = str( items ) + '__'
        if ( self.gccs == 'PU' ):
            if self.checkRECOMiniAOD3.isChecked(): # pmx
                option_regexp += ',PUpmx'
            else:
                option_regexp += ',PU'
#        print "**********", items, "- ", option_release_1 # to be removed
        (liste_fichiers_1) = cmd_fetch(option_is_from_data, option_release_1, option_regexp, option_mthreads, option_dry_run)
        self.rel_list += liste_fichiers_1
        
#    print "\n****** cleaning ******"
    self.rel_list = clean_collections(self, self.rel_list, self.gccs)
    self.ref_list = clean_collections(self, self.ref_list, self.gccs)
#    print "****** done ******"
    
    # si on veut comparer deux releases par fichiers DQM
    # self.listeReference.currentText() pour la reference
    #print "reference : ", self.listeReference.currentText() # reste à extraire la release de reference
    #option_release = 'CMSSW_7_2_0_pre4' # self.listeReference.currentText()    
    #cmd_fetch(option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run)

    #affichage des fichiers (n'affiche que la derniere recherche)
#    print '\n-----'
#    for items in self.rel_list:
#        print items
#        print explode_item(items)
#    print '-----'
#    for items in self.ref_list:
#        print items

    return 

def explode_item(item):
    # initial file name : DQM_V0001_R000000001__RelValTTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1__DQMIO.root
    # prefix in DQM_V0001_R000000001__ removed : RelValTTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1__DQMIO.root
    # suffix in __DQMIO.root removed : RelVal
    # new prefix in RelVal removed : TTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1
    # splitting with __ : TTbar_13 CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1
    # splitting second term with - : TTbar_13 CMSSW_7_4_0_pre8 PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1
    
#    print "explode item : ", item
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

def list_simplify(tablo):
    # simplification of tablo and self.ref_list_mod
    # WARNING : test before about len() = 1 -> do nothing

    temp = []
    item_line = tablo[0]
    temp2 = [item_line[2]]
    temp3 = [item_line[3]]
    
    item_line = ( tablo[0][0], tablo[0][1], [ tablo[0][2] ], [ tablo[0][3] ] )
#    print "\nlist_simplify : ", item_line

#    print "list_simplify : longueur tablo : ", len(tablo)
    if ( len(tablo) == 1 ):
        item_line = ( tablo[0][0], tablo[0][1], [ tablo[0][2] ], [ tablo[0][3] ] )
#        print "item_line : ", item_line
        
#    for items in tablo:
#        print "list_simplify - debut : ", items  
    for i in range(1, len(tablo)-0):
#        print "i = ", i
        (t, u, v, w) = tablo[i]
        if ( t == item_line[0]):
            if (u == item_line[1]):
                temp2.append(v)
                temp3.append(w)
                item_line = (item_line[0], item_line[1], temp2, temp3 )
                if ( i == len(tablo)-1 ):
                    temp.append(item_line)
            else :
                temp2 = (item_line[0], item_line[1], temp2) # to be removed ?
                temp.append(item_line)
                item_line = ( tablo[i][0], tablo[i][1], [ tablo[i][2] ], [ tablo[i][3] ] )
                temp2 = item_line[2]
                temp3 = item_line[3]
#                print "new item_line a : ", item_line
                if ( i == len(tablo)-1 ):
                    temp.append(item_line)
        else:
            temp.append(item_line)
            item_line = ( tablo[i][0], tablo[i][1],  [ tablo[i][2] ], [ tablo[i][3] ]  )
            temp2 = item_line[2]
            temp3 = item_line[3]
#            print "new item_line a : ", item_line
            if ( i == len(tablo)-1 ):
                temp.append(item_line)
    
#    print "longueur tablo : ", len(temp)
    if ( len(temp) == 0):
        temp.append(item_line)

#    for items in temp:
#        print "list_simplify - fin : ", items  
    
    return temp
      
def compare_datasets(t1, t2):
    import re
    temp = []
#    print "compare datasets"
    i = 0

    for it1 in t1:
        it11 = it1.replace('Startup', '')
        it11 = (it11.replace('_', '')).upper()
        for it2 in t2:
            it21 = (it2.replace('_', '')).upper()
            # to be continued avec re.search
            if ( re.search(it11, it21) ):
#                print "search : ", it11, " ", it21
                it22 = it21[-2:]
                temp.append([it1, it2]) # UP15
#                if ( ( it22 == '13' ) or ( it22 == '15' ) ): # UP15
#                    temp.append([it1, it2])                  # UP15
#                else:                                        # UP15
#                    print "KO : ", it22, it2, it1            # UP15
    
    return temp

def create_file_list(tablo):
    temp = []
    print "\ncreate_file_list", tablo
#    part_1 = tablo[0]
#    part_2 = tablo[1]
    itl2 = tablo[2]
    itl3 = tablo[3]
#    print "create_file_list itl2", itl2
#    print "create_file_list itl3", itl3
#    print "create_file_list :", itl3
#    name_base = "DQM_V0001_R000000001__RelVal" 
#    name_suffix = "__" + part_1 + "-" + part_2 + "__DQMIO.root"
    i = 0
    for part_3 in itl2:
#        print "create_file_list %d : %s \n"% (i, part_3)
#        name_rel = name_base + part_3 + name_suffix
#        temp.append([part_3, name_rel])
        temp.append([part_3, itl3[i] ])
        i += 1
    return temp

def create_commonfile_list(t1, t2):
    import re
    temp = []
#    print "create commonfile list"
    for it1 in t1:
        for it2 in t2:
#            print it1, it2
            if (it1[0] == it2[0]):
#                print "create commeon file list : ", it1, it2
                temp.append([it1[0], it1[1], it2[1]])
    
    return temp

def clean_files_list(t1, t2):
    temp = []
#    print "clean_files_list"
    for it1 in t1:
#        print "clean : ",it1[0], it1[1]
        for it2 in t2:
#            print "clean : ", it2, it1[1], it2[0]
            if ( it1[1] == it2[0] ):
#                print 'ok'
                tmp = [it1[0], it1[1], it2[1], it2[2]]
                temp.append(tmp)
    return temp

def write_OvalFile(self, t_rel_default_text, to_transmit_rel, to_transmit_ref):
    import os,sys,subprocess,glob,re,shutil
    
    # get collections list to do (Pt35, Pt10, TTbar, .... if checked)
    self.coll_list = get_collection_list(self)
    dataset_resume = compare_datasets(self.coll_list, self.my_choice_rel[2])
#    print "dataset_resume : ", dataset_resume
    if ( self.files_list ):
        self.files_list = clean_files_list(dataset_resume, self.files_list)
    else:
        itl2 = create_file_list(self.choice_rel)
        itf2 = create_file_list(self.choice_ref)
        self.files_list = create_commonfile_list(itl2, itf2) # attention on ne compare pas la longueur des tableaux
        self.files_list = clean_files_list(dataset_resume, self.files_list)
    
    for items in self.files_list:
        print "--", items, len(items)
        for it in items:
            print "--", it

    (tag_startup, data_version) = to_transmit_rel.split('-')
    if self.gccs == 'Fast':
        tag_startup = tag_startup[:-8]
    if self.gccs == 'PU':
        len_prefix = len(tag_startup.split('_')[0])+1
        tag_startup = tag_startup[len_prefix:]
    
    file = open("OvalFile", "w+") # default : overwrite the OvalFile
#    file = open("newfile.txt", "w+") # default : overwrite the OvalFile
    file.write('<var name="TEST_COMMENT" value="">\n')
    print 't rel default : ' , t_rel_default_text
    tmp = '<var name="TEST_NEW" value="' + t_rel_default_text + '">\n'
    file.write(tmp) 
    print 't ref default : ' , self.lineedit3.text()[6:] + self.getPublish.text_ext
    tmp = '<var name="TEST_REF" value="' + self.lineedit3.text()[6:] + self.getPublish.text_ext + '">\n'
    if self.checkRECOMiniAOD3.isChecked():
        print 't ref default : ' , self.lineedit1.text()[6:] + self.getPublish.text_ext
        tmp = '<var name="TEST_REF" value="' + self.lineedit1.text()[6:] + self.getPublish.text_ext + '">\n'
    file.write(tmp) 
    tmp = '\n<var name="TAG_STARTUP" value="' + tag_startup + '">\n'
    tmp += '<var name="DATA_VERSION" value="' + data_version + '">\n\n'
    file.write(tmp)
    tmp = 'TAG for the REFERENCE DATA, USED ONLY FOR INFORMATION ON WEB PAGE\n'
    file.write(tmp)
    tmp = '<var name="DD_COND_REF" value="' + to_transmit_ref + '">\n\n'
    file.write(tmp) 
    tmp = '<var name="DD_RELEASE" value="${CMSSW_VERSION}">\n\n'
    file.write(tmp)
    tmp = '<var name="STORE_DIR" value="' + os.getcwd() + '">\n'
    tmp += '<var name="STORE_REF" value="' + os.getcwd() + '">\n\n'
    
    if self.getPublish.radio21_P.isChecked():
        print 'ovalfile local'
        web_dir_path = self.working_dir_base
        tmp += '<var name="WEB_DIR" value="' + web_dir_path + '">\n\n'
    if self.getPublish.radio22_P.isChecked():
        print 'ovalfile external'
        web_dir_path = '"/afs/cern.ch/cms/Physics/egamma/www/validation/Electrons/'
#        web_dir_path = '"/eos/project/c/cmsweb/www/egamma/validation/Electrons/'
#        web_dir_path = ''
#        if ( self.getPublish.text_ext == "_dev" ):
        print 'extension : ', self.getPublish.text_ext
        if ( re.search('_dev', self.getPublish.text_ext) ):
            tmp += '<var name="WEB_DIR" value=' + web_dir_path + 'Dev">\n\n'
        if ( re.search('_DQM_std', self.getPublish.text_ext) ):
#        if ( self.getPublish.text_ext == "_DQM_std" ):
            tmp += '<var name="WEB_DIR" value=' + web_dir_path + 'Releases">\n\n'

#        tmp += '<var name="WEB_DIR" value="/afs/cern.ch/cms/Physics/egamma/www/validation/Electrons/Releases">\n\n'
    file.write(tmp)
    tmp = 'The value of OVAL_ENVNAME is automatically set by Oval to the name\n'
    tmp += 'of the current environment, before running any executable. Using it below,\n'
    file.write(tmp)
    tmp = 'we have an output file name which is unique for each execution.\n\n<var name="TEST_OUTPUT_LOGS" value="*.${OVAL_ENVNAME}.olog">\n\n'
    file.write(tmp)
    tmp = 'Oval is able to check the output channel of an execution and compare it with a reference output.\n'
    tmp += 'The tags below are defining which are lines to be compared. The currently specification is a\n'
    tmp += 'first draft, and we do not yet check the differences that Oval could raise.\n\n'
    tmp += '<diffnumber expr="^dataset has (\d+) files:$" tolerance="1">\n<error expr="^dataset has 0 files:$">\n\n'
    file.write(tmp)
    tmp = '<diffline expr="^(TH1.Print Name = [a-zA-Z_]+, Entries= ).*$">\n'
    tmp += '<diffnumber expr="^TH1.Print Name = [a-zA-Z_]+, Entries= (\d+),.*$" tolerance="20%">\n'
    tmp += '<diffnumber expr="^TH1.Print Name = [a-zA-Z_]+, Entries= \d+, Total sum= (\S+)$" tolerance="10%">\n'
    tmp += '<diffline expr="^(h_\S+ has )\d+ entries of mean value \S+$">\n'
    tmp += '<diffnumber expr="^h_\S+ has (\d+) entries of mean value \S+$" tolerance="20%">\n'
    tmp +='<diffnumber expr="^h_\S+ has \d+ entries of mean value (\S+)$" tolerance="10%">\n'
    tmp += '<!diffvar name="HISTO" expr="^TH1.Print Name = [a-zA-Z_]+, Entries= \d+, Total sum= (\S+)$" tolerance="10%">\n\n'
    file.write(tmp)
    tmp = '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n'
    tmp += '================================================================================\n'
    if self.gccs == 'Fast':
        tmp += 'FastSim\n'
    else :
        tmp += 'FullSim\n'
    tmp += '================================================================================\n'
    tmp += '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n'
    file.write(tmp)
    if self.gccs == 'Full':
        tmp = '<environment name="FullStdStats">\n\n'
    elif self.gccs == 'PU':
        tmp = '<environment name="FullStdStats">\n\n'
    else :
        tmp = '<environment name="FastSim">\n\n'

    tmp += '  This set of targets is currently used for the validation of electrons.\n\n'
    tmp += '  Used if DD_source=/eos/...\n'
    if self.gccs == 'Fast':
        tmp += '  <var name="DD_TIER" value="GEN-SIM-DIGI-RECO">\n\n'
        tmp += '  <var name="VAL_HISTOS" value="ElectronMcSignalHistos.txt">\n'
        tmp += '  <var name="VAL_CONFIGURATION" value="ElectronMcSignalValidation_cfg">\n'
        tmp += '  <var name="VAL_CONFIGURATION_gedGsfE" value="ElectronMcSignalValidation_gedGsfElectrons_cfg">\n'
        tmp += '  <var name="VAL_POST_CONFIGURATION" value="ElectronMcSignalPostValidation_cfg">\n\n'
    else :
        if self.checkRECOMiniAOD2.isChecked():
            tmp += '  <var name="DD_TIER" value="MINIAODSIM">\n\n'
            tmp += '  <var name="VAL_HISTOS" value="ElectronMcSignalHistosMiniAOD.txt">\n'
            tmp += '  <var name="VAL_CONFIGURATION" value="ElectronMcSignalValidationMiniAOD_cfg">\n'
            tmp += '  <var name="VAL_CONFIGURATION_gedGsfE" value="ElectronMcSignalValidationMiniAOD_cfg">\n'
            tmp += '  <var name="VAL_POST_CONFIGURATION" value="ElectronMcSignalPostValidationMiniAOD_cfg">\n\n'
        else:
            tmp += '  <var name="DD_TIER" value="GEN-SIM-RECO">\n\n'
            tmp += '  <var name="VAL_HISTOS" value="ElectronMcSignalHistos.txt">\n'
            tmp += '  <var name="VAL_CONFIGURATION" value="ElectronMcSignalValidation_cfg">\n'
            tmp += '  <var name="VAL_CONFIGURATION_gedGsfE" value="ElectronMcSignalValidation_gedGsfElectrons_cfg">\n'
            tmp += '  <var name="VAL_POST_CONFIGURATION" value="ElectronMcSignalPostValidation_cfg">\n\n'
    file.write(tmp)

    if self.gccs == 'Full': # FULLSIM
        tmp = '  <environment name="ValFullgedvsged">\n\n'
        file.write(tmp)
        tmp = '    <var name="TEST_GLOBAL_TAG" value="${TAG_STARTUP}">\n'
        tmp += '    <var name="TEST_GLOBAL_AUTOCOND" value="startup">\n'
        tmp += '    <var name="DD_COND" value="${TEST_GLOBAL_TAG}-${DATA_VERSION}">\n\n'
        file.write(tmp)
        tmp = ''
        tmp += '    <environment name="Valdummy">\n\n'
        tmp += '      <var name="DD_SAMPLE" value="dummy">\n\n'
        tmp += '        <var name="RED_FILE" value="DQM_DUMMY.root">\n'
        tmp += ' <var name="BLUE_FILE" value="DQM_DUMMY.root">\n'
        tmp += ' <target name="publish" cmd=\'electronCompare.py -c ${VAL_HISTOS} -r ${RED_FILE} -b ${BLUE_FILE} '
        tmp += '-t "${TEST_NEW} / gedGsfElectrons / ${DD_SAMPLE} / ${DD_COND} vs ${TEST_REF} / gedGsfElectrons / ${DD_SAMPLE} / ${DD_COND_REF}" '
        tmp += '${STORE_DIR}/${RED_FILE} ${STORE_REF}/${BLUE_FILE} ${WEB_DIR}/${TEST_NEW}/GedvsGed_${TEST_REF}/Fullgedvsged_${DD_SAMPLE}_gedGsfE_Startup\'>\n\n'
        tmp += '    </environment>\n\n'
        file.write(tmp)

        for items in self.files_list:
            print items[1]
            tmp = ''
            tmp += '      <environment name="ValgedvsgedFull' + items[0] + '_gedGsfE">\n\n'
            tmp += '        <var name="DD_SAMPLE" value="RelVal' + items[1] + '">\n\n'
            if ( re.search('Pt1000', items[1]) ):
                print 'OvalFile : Pt1000\n'
                tmp += '      <var name="VAL_HISTOS" value="ElectronMcSignalHistosPt1000.txt">\n'
                tmp += '      <var name="VAL_ANALYZER" value="ElectronMcSignalValidatorPt1000">\n'
                tmp += '      <var name="VAL_POST_ANALYZER" value="ElectronMcSignalPostValidatorPt1000">\n'
                tmp += '      <var name="VAL_CONFIGURATION_gedGsfE" value="ElectronMcSignalValidationPt1000_gedGsfElectrons_cfg">\n'
                tmp += '      <var name="VAL_POST_CONFIGURATION" value="ElectronMcSignalPostValidationPt1000_cfg">\n'
            if ( re.search('QCD', items[1]) ):
                print 'OvalFile : QcdPt80120Startup_13\n'
                tmp += '      <var name="VAL_HISTOS" value="ElectronMcFakeHistos.txt">\n'
                tmp += '      <var name="VAL_ANALYZER" value="ElectronMcFakeValidator">\n'
                tmp += '      <var name="VAL_POST_ANALYZER" value="ElectronMcFakePostValidator">\n'
                tmp += '      <var name="VAL_CONFIGURATION_gedGsfE" value="ElectronMcFakeValidation_gedGsfElectrons_cfg">\n'
                tmp += '      <var name="VAL_POST_CONFIGURATION" value="ElectronMcFakePostValidation_cfg">\n'
                
            tmp += '        <var name="RED_FILE" value="' + items[2] + '">\n'
            tmp += '        <var name="BLUE_FILE" value="' + str(self.lineedit3.text()[6:]) + '/' + items[3] + '">\n'
            tmp += '        <target name="publish" cmd=\'electronCompare.py -c ${VAL_HISTOS} -r ${RED_FILE} -b ${BLUE_FILE} '
            tmp += '-t "gedGsfElectrons ${DD_SAMPLE}<br><b><font color=\'red\'>${TEST_NEW}</font></b> : ${DD_COND}<br><b><font color=\'blue\'>${TEST_REF}</font></b> : ${DD_COND_REF}" '
            tmp += '${STORE_DIR}/${RED_FILE} ${STORE_REF}/${BLUE_FILE} ${WEB_DIR}/${TEST_NEW}/GedvsGed_${TEST_REF}/Fullgedvsged_${DD_SAMPLE}_gedGsfE_Startup\'>\n\n'
#            tmp += '-t "${TEST_NEW} / gedGsfElectrons / ${DD_SAMPLE} / ${DD_COND} vs ${TEST_REF} / gedGsfElectrons / ${DD_SAMPLE} / ${DD_COND_REF}" '
#            tmp += '${STORE_DIR}/${RED_FILE} ${STORE_REF}/${BLUE_FILE} ${WEB_DIR}/${TEST_NEW}/GedvsGed_${TEST_REF}/Fullgedvsged_${DD_SAMPLE}_gedGsfE_Startup\'>\n\n'
            tmp += '      </environment>\n\n'
            file.write(tmp)
        tmp = '  </environment>\n\n' 
        tmp += '</environment>\n'
        file.write(tmp)
    elif self.gccs == 'PU': # PU
        tmp = '  <environment name="ValPileUpStartup">\n\n'
        tmp += '    <var name="TAG_STARTUP" value="${TAG_STARTUP}">\n'
        file.write(tmp)
        tmp = '    <var name="TEST_GLOBAL_TAG" value="${TAG_STARTUP}">\n'
        tmp += '    <var name="TEST_GLOBAL_AUTOCOND" value="startup">\n\n'
#        tmp += '    <var name="DD_COND" value="PU_${TEST_GLOBAL_TAG}-${DATA_VERSION}">\n\n'
        file.write(tmp)
        tmp = ''
        tmp += '    <environment name="Valdummy">\n\n'
        tmp += '      <var name="DD_SAMPLE" value="dummy">\n\n'
        tmp += '        <var name="RED_FILE" value="DQM_DUMMY.root">\n'
        tmp += ' <var name="BLUE_FILE" value="DQM_DUMMY.root">\n'
        tmp += ' <target name="publish" cmd=\'electronCompare.py -c ${VAL_HISTOS} -r ${RED_FILE} -b ${BLUE_FILE} '
        tmp += '-t "gedGsfElectrons ${DD_SAMPLE}<br><b><font color=\'red\'>${TEST_NEW}</font></b> : ${DD_COND}<br><b><font color=\'blue\'>${TEST_REF}</font></b> : ${DD_COND_REF}" '
        tmp += '${STORE_DIR}/${RED_FILE} ${STORE_REF}/${BLUE_FILE} ${WEB_DIR}/${TEST_NEW}/GedvsGed_${TEST_REF}/Fullgedvsged_${DD_SAMPLE}_gedGsfE_Startup\'>\n\n'
#        tmp += '-t "${TEST_NEW} / gedGsfElectrons / ${DD_SAMPLE} / ${DD_COND} vs ${TEST_REF} / gedGsfElectrons / ${DD_SAMPLE} / ${DD_COND_REF}" '
#        tmp += '${STORE_DIR}/${RED_FILE} ${STORE_REF}/${BLUE_FILE} ${WEB_DIR}/${TEST_NEW}/GedvsGed_${TEST_REF}/Fullgedvsged_${DD_SAMPLE}_gedGsfE_Startup\'>\n\n'
        tmp += '    </environment>\n\n'
        file.write(tmp)
        for items in self.files_list:
#            print items[0]
#            print items[2]
            it_tmp = explode_item(items[2])
            prefix = it_tmp[2].split('_')[0]
            print "PU prefix " , items[2], ' - ', prefix
            tmp = ''
            tmp += '    <var name="DD_COND" value="' + prefix + '_${TEST_GLOBAL_TAG}-${DATA_VERSION}">\n\n'
            tmp += '    <var name="DD_COND_REF" value="' + to_transmit_ref + '">\n\n'
            tmp += '      <environment name="ValPileUp' + items[0] + '_gedGsfE">\n\n'
            tmp += '        <var name="DD_SAMPLE" value="RelVal' + items[1] + '">\n\n'
            tmp += '      <var name="RED_FILE" value="' + items[2] + '">\n'
            tmp += '      <var name="BLUE_FILE" value="' + str(self.lineedit3.text()[6:]) + '/' + items[3] + '">\n\n'
            tmp += '      <target name="publish" cmd=\'electronCompare.py -c ${VAL_HISTOS} -r ${RED_FILE} -b ${BLUE_FILE} '
            tmp += '-t "gedGsfElectrons ${DD_SAMPLE}<br><b><font color=\'red\'>${TEST_NEW}</font></b> : ${DD_COND}<br><b><font color=\'blue\'>${TEST_REF}</font></b> : ${DD_COND_REF}" '
            tmp += '${STORE_DIR}/${RED_FILE} ${STORE_REF}/${BLUE_FILE} ${WEB_DIR}/${TEST_NEW}/GedvsGed_${TEST_REF}/' + prefix + '_${DD_SAMPLE}_gedGsfE_Startup\'>\n\n'
#            tmp += '-t "${TEST_NEW} / gedGsfElectrons / ${DD_SAMPLE} / ${DD_COND} vs ${TEST_REF} / gedGsfElectrons / ${DD_SAMPLE} / ${DD_COND_REF}" '
#            tmp += '${STORE_DIR}/${RED_FILE} ${STORE_REF}/${BLUE_FILE} ${WEB_DIR}/${TEST_NEW}/GedvsGed_${TEST_REF}/' + prefix + '_${DD_SAMPLE}_gedGsfE_Startup\'>\n\n'
            tmp += '      </environment>\n\n'
            file.write(tmp)
        tmp = '  </environment>\n\n' 
        tmp += '</environment>\n'
        file.write(tmp)
    else : # FASTSIM
        tmp = '  <environment name="ValFastVsFast">\n\n' # environment ValFastVsFast
        tmp += '    <environment name="ValFastVsFastStartup">\n\n' # environment ValFastVsFastStartup
        file.write(tmp)
        tmp = '      <var name="TEST_GLOBAL_TAG" value="${TAG_STARTUP}">\n'
        tmp += '      <var name="TEST_GLOBAL_AUTOCOND" value="startup">\n'
        tmp += '      <var name="DD_COND" value="${TEST_GLOBAL_TAG}_FastSim-${DATA_VERSION}">\n\n'
        file.write(tmp)
        for items in self.files_list:
            print "fast vs fast : ", items
            tmp = ''
            tmp += '      <environment name="ValFastVsFast' + items[0] + '_gedGsfE">\n\n' # environment DD_SAMPLE
            tmp += '        <var name="DD_SAMPLE" value="RelVal' + items[1] + '">\n\n'
            tmp += '      <var name="RED_FILE" value="' + items[2] + '">\n'
            tmp += '      <var name="BLUE_FILE" value="' + str(self.lineedit3.text()[6:]) + '/' + items[3] + '">\n'
            tmp += '      <target name="publish" cmd=\'electronCompare.py -c ${VAL_HISTOS} -r ${RED_FILE} -b ${BLUE_FILE} '
            tmp += '-t "Fast vs Fast ${DD_SAMPLE} <br><b><font color=\'red\'>${TEST_NEW}</font></b> : ${DD_COND}<br><b><font color=\'blue\'>${TEST_REF}</font></b> : ${DD_COND_REF}" '
            tmp += '${STORE_DIR}/${RED_FILE} ${STORE_REF}/${BLUE_FILE} ${WEB_DIR}/${TEST_NEW}/FastVsFast_${TEST_REF}/Fast_${DD_SAMPLE}_Startup\'>\n\n'
#            tmp += '-t "${TEST_NEW} / ${DD_SAMPLE} / ${DD_COND} vs ${TEST_REF} / ${DD_SAMPLE} / ${DD_COND_REF}" '
#            tmp += '${STORE_DIR}/${RED_FILE} ${STORE_REF}/${BLUE_FILE} ${WEB_DIR}/${TEST_NEW}/FastVsFast_${TEST_REF}/Fast_${DD_SAMPLE}_Startup\'>\n\n'
            tmp += '      </environment>\n\n'                                             # environment DD_SAMPLE
            file.write(tmp)
        tmp = '  </environment>\n\n'                               # environment ValFastVsFastStartup
        tmp += ' </environment>\n\n'                               # environment ValFastVsFast

        file.write(tmp)
        tmp = '  <environment name="ValFastVsFull">\n\n'
        tmp += '    <environment name="ValFastVsFullStartup">\n\n' # environment ValFastVsFullStartup
        file.write(tmp)
        tmp = '      <var name="TEST_GLOBAL_TAG" value="${TAG_STARTUP}">\n'
        tmp += '      <var name="TEST_GLOBAL_AUTOCOND" value="startup">\n'
        tmp += '      <var name="DD_COND" value="${TEST_GLOBAL_TAG}_FastSim-${DATA_VERSION}">\n\n'
        file.write(tmp)
        for items in self.files_list:
            print "fast vs full : ", items
            print items[0]
            print "red file : ", items[2]
            it_tmp = items[2].replace('_FastSim', '')
            dd_cond_full = explode_item(it_tmp)
            print "OVALFILE FAST " , dd_cond_full, ' - ', it_tmp, ' - ', dd_cond_full[2]
            print "blue file : ", it_tmp
            print "self.FastvsFastTag :", self.FastvsFastTag
            print "self.FastvsFullTag :", self.FastvsFullTag
            it_tmp2 = it_tmp.replace(self.FastvsFastTag, self.FastvsFullTag)
            print "blue file :", it_tmp2
            tmp = ''
            tmp += '      <environment name="ValFastVsFull' + items[0] + '_gedGsfE">\n\n' # environment DD_SAMPLE
            tmp += '        <var name="DD_SAMPLE" value="RelVal' + items[1] + '">\n\n'
            tmp += '      <var name="RED_FILE" value="' + items[2] + '">\n'
            tmp += '      <var name="BLUE_FILE" value="' + it_tmp2 + '">\n'
            tmp += '      <target name="publish" cmd=\'electronCompare.py -c ${VAL_HISTOS} -r ${RED_FILE} -b ${BLUE_FILE} '
            tmp += '-t "Fast vs Full ${DD_SAMPLE} <br><b><font color=\'red\'>${TEST_NEW}</font></b> : ${DD_COND}<br><b><font color=\'blue\'>${TEST_NEW}</font></b> : ' + self.FastvsFullTag + '" ' 
            tmp += '${STORE_DIR}/${RED_FILE} ${STORE_REF}/${BLUE_FILE} ${WEB_DIR}/${TEST_NEW}/FastVsFull/${DD_SAMPLE}_Startup\'>\n\n'
            tmp += '      </environment>\n\n'                                             # environment DD_SAMPLE
            file.write(tmp)
        tmp = '  </environment>\n\n'                               # environment ValFastVsFullStartup
        tmp += ' </environment>\n\n'                               # environment ValFastVsFull
        
        tmp += '</environment>\n'
        file.write(tmp)
        
    file.close()
    shutil.copy('OvalFile', self.working_dir_base) # copy OvalFile for executing jobs

    return True