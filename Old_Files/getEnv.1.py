#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys
import urllib2

class env:
    def __init__(self): 
        self.CMSSWBASE = os.environ['CMSSW_BASE'] # donne le repertoire de travail
        self.CMSSWBASECMSSWRELEASEBASE = os.environ['CMSSW_RELEASE_BASE'] # donne la release et l'architecture
        self.CMSSWBASECMSSWVERSION = os.environ['CMSSW_VERSION'] # donne la release (CMSSW_7_1_0 par exemple)

    def getCMSSWBASE(self):
        CMSSWBASE = os.environ['CMSSW_BASE']
        return CMSSWBASE
		
    def getCMSSWBASECMSSWRELEASEBASE(self):
        return self.CMSSWBASECMSSWRELEASEBASE
		
    def getCMSSWBASECMSSWVERSION(self):
        return self.CMSSWBASECMSSWVERSION
		
    def cmsAll(self):
        cmsAll="<strong>CMSSW_BASE</strong> : " + self.getCMSSWBASE()
        cmsAll+="<br /><strong>CMSSW_RELEASE_BASE</strong> : " + self.getCMSSWBASECMSSWRELEASEBASE()
        cmsAll+="<br /><strong>CMSSW_VERSION</strong> : " + self.getCMSSWBASECMSSWVERSION()
        return cmsAll

    def eosText(self):
        eosText="/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select"
        eosText+=' ls /eos/cms/store/relval/' + self.getCMSSWBASECMSSWVERSION()
        return eosText

    def eosFind(self):
        eosFind="http://cms-project-relval.web.cern.ch/cms-project-relval/relval_stats/"
        return eosFind

    def eosStore(self):
        eosStore="http://cmsdoc.cern.ch/cms/Physics/egamma/www/validation/Electrons/Store/"
        return eosStore
		
    def liste_Gsf(self):
        liste_Gsf = ['RelValSingleElectronPt10', 'RelValSingleElectronPt1000', 'RelValSingleElectronPt35', 'RelValQCD_Pt_80_120', 'RelValTTbar', 'RelValZEE']
        return liste_Gsf

    def liste_ged(self):
        liste_ged = ['RelValSingleElectronPt10_UP15', 'RelValSingleElectronPt1000_UP15', 'RelValSingleElectronPt35_UP15', 'RelValQCD_Pt_80_120_13', 'RelValTTbar_13', 'RelValZEE_13']
        return liste_ged

    def liste_fastpu(self):
        liste_fastpu = ['RelValTTbar_13', 'RelValZEE_13']
        return liste_fastpu

    def liste_type(self):
        liste_type = ['GEN-SIM-RECO', 'GEN-SIM-DIGI-RECO']
        return liste_type

    def liste_etapes(self):
        liste_etapes = ['analyze', 'finalize', 'store', 'publish']
        return liste_etapes

    def liste_interaction(self):
        liste_interaction = ['batch', 'interactif']
        return liste_interaction

    def liste_calcul(self):
        liste_calcul = ['FULL', 'PU', 'FAST']
        return liste_calcul
