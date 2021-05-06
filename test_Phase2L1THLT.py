import FWCore.ParameterSet.Config as cms

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('analysis')
options.register('filterOutput',True,options.multiplicity.singleton,options.varType.bool,"filter the outputed edm")
options.register('runL1HPSTaus',True,options.multiplicity.singleton,options.varType.bool,"runL1HPSTaus")
options.register('runL1NNTaus',True,options.multiplicity.singleton,options.varType.bool,"runL1NNTaus")
options.register('reducedEvt',False,options.multiplicity.singleton,options.varType.bool,"output reduced event content")
options.register('l1OnlyEvt',False,options.multiplicity.singleton,options.varType.bool,"l1 only event content")
options.register('runOnExisting',False,options.multiplicity.singleton,options.varType.bool,"dont rerun the l1 but take existing values")

options.register('nrThreads',2,options.multiplicity.singleton,options.varType.int,"number of threads to use")
options.parseArguments()

if options.runOnExisting:
    process = cms.Process("L1TReSkiming")
else:
    process = cms.Process("L1TSkimming")

### Basic loads
process.load("Configuration.StandardSequences.Services_cff")
process.load("FWCore.MessageService.MessageLogger_cfi")
### GlobalTag
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag

process.GlobalTag = GlobalTag(process.GlobalTag, "111X_mcRun4_realistic_T15_v4", "")

### Rationale: we have to build this configuration file on top
### of something. We choose to do it on top of EGamma,
### since at this point in time (Feb-21) the Muon and JetMET
### customisations are fairly simple

### Reference: https://gitlab.cern.ch/sharper/EgHLTPhase2/-/blob/master/Menus/egammaBasicMenu.py

### Load the setup a la EGamma
### Notice that you should have followed the setup here:
### https://gitlab.cern.ch/sharper/EgHLTPhase2/-/tree/master

import HLTrigger.PhaseII.EGamma.Tools.hlt_config_tools as eghlt_tools

eghlt_tools.load_all(process, "HLTrigger.PhaseII.EGamma.PSets")
process.load("HLTrigger.PhaseII.EGamma.ESSources.essources_cff")
process.load("HLTrigger.PhaseII.EGamma.ESProducers.esproducers_cff")
process.load("HLTrigger.PhaseII.EGamma.ESProducers.esproducers_hlt_cff")
process.prefer("siPixelFakeGainOfflineESSource")
process.prefer("hltTTRBWR")
process.es_prefer_ppsDBESSource = cms.ESPrefer("PoolDBESSource", "ppsDBESSource")
process.es_prefer_hcalHardcode = cms.ESPrefer("HcalHardcodeCalibrations", "es_hardcode")

process.maxEvents = cms.untracked.PSet(
    input=cms.untracked.int32(options.maxEvents),
    output=cms.optional.untracked.allowed(cms.int32, cms.PSet),
)

process.options = cms.untracked.PSet(
    numberOfStreams = cms.untracked.uint32(options.nrThreads),
    numberOfThreads = cms.untracked.uint32(options.nrThreads),
    wantSummary = cms.untracked.bool(True)
)

### Input source
process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring()
)
eghlt_tools.setInputFiles(process,inputFiles=options.inputFiles,verbose=False)

### L1T ###
process.load("HLTrigger.PhaseII.EGamma.Sequences.HLTL1Sequence_cff")

### MUON ###

### Reference: https://github.com/khaosmos93/CMSPhase2MuonHLT/blob/master/example_cfgs/HLT_Phase2_example_menu.py
### Set the L1Tracks explicitly
process.L1TkMuons.L1TrackInputTag = cms.InputTag(
    "TTTracksFromTrackletEmulation", "Level1TTTracks", "RECO"
)
### Apply quality cuts by default
process.L1TkMuons.applyQualityCuts = cms.bool(True)

process.hltL1TkSingleMuFiltered22 = cms.EDFilter(
    "L1TTkMuonFilter",
    MaxEta=cms.double(2.4),
    MinEta=cms.double(-2.4),
    MinN=cms.int32(1),
    MinPt=cms.double(22.0),
    Scalings=cms.PSet(
        barrel=cms.vdouble(0.820128, 1.04124, 0.0),
        endcap=cms.vdouble(0.864715, 1.03215, 0.0),
        overlap=cms.vdouble(0.920897, 1.03712, 0.0),
    ),
    inputTag=cms.InputTag("L1TkMuons", "", "L1TSkimming"),
    saveTags=cms.bool(True),
)

process.hltL1TkSingleMuFiltered15 = cms.EDFilter(
    "L1TTkMuonFilter",
    MaxEta=cms.double(2.4),
    MinEta=cms.double(-2.4),
    MinN=cms.int32(1),
    MinPt=cms.double(15.0),
    Scalings=cms.PSet(
        barrel=cms.vdouble(0.820128, 1.04124, 0.0),
        endcap=cms.vdouble(0.864715, 1.03215, 0.0),
        overlap=cms.vdouble(0.920897, 1.03712, 0.0),
    ),
    inputTag=cms.InputTag("L1TkMuons", "", "L1TSkimming"),
    saveTags=cms.bool(True),
)

process.hltL1TkDoubleMuFiltered7 = cms.EDFilter(
    "L1TTkMuonFilter",
    MaxEta=cms.double(2.4),
    MinEta=cms.double(-2.4),
    MinN=cms.int32(2),
    MinPt=cms.double(7.0),
    Scalings=cms.PSet(
        barrel=cms.vdouble(0.820128, 1.04124, 0.0),
        endcap=cms.vdouble(0.864715, 1.03215, 0.0),
        overlap=cms.vdouble(0.920897, 1.03712, 0.0),
    ),
    inputTag=cms.InputTag("L1TkMuons", "", "L1TSkimming"),
    saveTags=cms.bool(True),
)

process.hltDoubleMuon7DZ1p0 = cms.EDFilter(
    "HLT2L1TkMuonL1TkMuonDZ",
    MaxDZ=cms.double(1.0),
    MinDR=cms.double(-1),
    MinN=cms.int32(1),
    MinPixHitsForDZ=cms.int32(0),
    checkSC=cms.bool(False),
    inputTag1=cms.InputTag("hltL1TkDoubleMuFiltered7"),
    inputTag2=cms.InputTag("hltL1TkDoubleMuFiltered7"),
    originTag1=cms.VInputTag("L1TkMuons::L1TSkimming"),
    originTag2=cms.VInputTag("L1TkMuons::L1TSkimming"),
    saveTags=cms.bool(True),
    triggerType1=cms.int32(-114),
    triggerType2=cms.int32(-114),
)

process.hltL1TripleMuFiltered3 = cms.EDFilter(
    "L1TTkMuonFilter",
    MaxEta=cms.double(2.4),
    MinEta=cms.double(-2.4),
    MinN=cms.int32(3),
    MinPt=cms.double(3.0),
    Scalings=cms.PSet(
        barrel=cms.vdouble(0.820128, 1.04124, 0.0),
        endcap=cms.vdouble(0.864715, 1.03215, 0.0),
        overlap=cms.vdouble(0.920897, 1.03712, 0.0),
    ),
    inputTag=cms.InputTag("L1TkMuons", "", "L1TSkimming"),
    saveTags=cms.bool(True),
)

process.hltL1SingleMuFiltered5 = cms.EDFilter(
    "L1TTkMuonFilter",
    MaxEta=cms.double(2.4),
    MinEta=cms.double(-2.4),
    MinN=cms.int32(1),
    MinPt=cms.double(5.0),
    Scalings=cms.PSet(
        barrel=cms.vdouble(0.820128, 1.04124, 0.0),
        endcap=cms.vdouble(0.864715, 1.03215, 0.0),
        overlap=cms.vdouble(0.920897, 1.03712, 0.0),
    ),
    inputTag=cms.InputTag("L1TkMuons", "", "L1TSkimming"),
    saveTags=cms.bool(True),
)

process.hltTripleMuon3DZ1p0 = cms.EDFilter(
    "HLT2L1TkMuonL1TkMuonDZ",
    MaxDZ=cms.double(1.0),
    MinDR=cms.double(-1),
    MinN=cms.int32(3),
    MinPixHitsForDZ=cms.int32(0),
    checkSC=cms.bool(False),
    inputTag1=cms.InputTag("hltL1TripleMuFiltered3"),
    inputTag2=cms.InputTag("hltL1TripleMuFiltered3"),
    originTag1=cms.VInputTag("L1TkMuons::L1TSkimming"),
    originTag2=cms.VInputTag("L1TkMuons::L1TSkimming"),
    saveTags=cms.bool(True),
    triggerType1=cms.int32(-114),
    triggerType2=cms.int32(-114),
)

process.hltTripleMuon3DR0 = cms.EDFilter(
    "HLT2L1TkMuonL1TkMuonMuRefDR",
    MinDR=cms.double(0),
    MinN=cms.int32(3),
    inputTag1=cms.InputTag("hltL1TripleMuFiltered3"),
    inputTag2=cms.InputTag("hltL1TripleMuFiltered3"),
    originTag1=cms.VInputTag("L1TkMuons::L1TSkimming"),
    originTag2=cms.VInputTag("L1TkMuons::L1TSkimming"),
    saveTags=cms.bool(True),
)

### EGAMMA ###

### Filters

process.L1TkEleSingle25Filter = cms.EDFilter(
    "L1TTkEleFilter",
    saveTags=cms.bool(True),
    MinPt=cms.double(25.0),
    MinN=cms.int32(1),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    inputTag1=cms.InputTag("L1TkElectronsEllipticMatchCrystal", "EG"),
    inputTag2=cms.InputTag("L1TkElectronsEllipticMatchHGC", "EG"),
    Qual1IsMask=cms.bool(True),
    Qual2IsMask=cms.bool(False),
    ApplyQual1=cms.bool(True),
    ApplyQual2=cms.bool(True),
    Quality1=cms.int32(0x2),
    Quality2=cms.int32(5),
    EtaBinsForIsolation=cms.vdouble(0.0, 1.479, 4.0),
    TrkIsolation=cms.vdouble(99999.0, 99999.0),
    Scalings=cms.PSet(  # for TkElectronOfflineEtCut, taken from PhaseIIL1TriggerMenuTools twiki
        barrel=cms.vdouble(0.805095, 1.18336, 0.0),
        endcap=cms.vdouble(0.453144, 1.26205, 0.0),
    ),
)

process.L1TkEleDouble12Filter = cms.EDFilter(
    "L1TTkEleFilter",
    saveTags=cms.bool(True),
    MinPt=cms.double(12.0),
    MinN=cms.int32(2),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    inputTag1=cms.InputTag("L1TkElectronsEllipticMatchCrystal", "EG"),
    inputTag2=cms.InputTag("L1TkElectronsEllipticMatchHGC", "EG"),
    Qual1IsMask=cms.bool(True),
    Qual2IsMask=cms.bool(False),
    ApplyQual1=cms.bool(True),
    ApplyQual2=cms.bool(True),
    Quality1=cms.int32(0x2),
    Quality2=cms.int32(5),
    EtaBinsForIsolation=cms.vdouble(0.0, 1.479, 4.0),
    TrkIsolation=cms.vdouble(99999.0, 99999.0),
    Scalings=cms.PSet(  # for TkElectronOfflineEtCut, taken from PhaseIIL1TriggerMenuTools twiki
        barrel=cms.vdouble(0.805095, 1.18336, 0.0),
        endcap=cms.vdouble(0.453144, 1.26205, 0.0),
    ),
)

process.L1TkEleSingle36Filter = cms.EDFilter(
    "L1TTkEleFilter",
    saveTags=cms.bool(True),
    MinPt=cms.double(36.0),
    MinN=cms.int32(1),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    inputTag1=cms.InputTag("L1TkElectronsEllipticMatchCrystal", "EG"),
    inputTag2=cms.InputTag("L1TkElectronsEllipticMatchHGC", "EG"),
    Qual1IsMask=cms.bool(True),
    Qual2IsMask=cms.bool(False),
    ApplyQual1=cms.bool(True),
    ApplyQual2=cms.bool(True),
    Quality1=cms.int32(0x2),
    Quality2=cms.int32(5),
    EtaBinsForIsolation=cms.vdouble(0.0, 1.479, 4.0),
    TrkIsolation=cms.vdouble(99999.0, 99999.0),
    Scalings=cms.PSet(  # for TkElectronOfflineEtCut, taken from PhaseIIL1TriggerMenuTools twiki
        barrel=cms.vdouble(0.805095, 1.18336, 0.0),
        endcap=cms.vdouble(0.453144, 1.26205, 0.0),
    ),
)

process.L1TkEmSingle37Filter = cms.EDFilter(
    "L1TTkEmFilter",
    saveTags=cms.bool(True),
    MinPt=cms.double(37.0),
    MinN=cms.int32(1),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    inputTag1=cms.InputTag("L1TkPhotonsCrystal", "EG"),
    inputTag2=cms.InputTag("L1TkPhotonsHGC", "EG"),
    Qual1IsMask=cms.bool(True),
    Qual2IsMask=cms.bool(False),
    ApplyQual1=cms.bool(True),
    ApplyQual2=cms.bool(True),
    Quality1=cms.int32(0x2),
    Quality2=cms.int32(5),
    EtaBinsForIsolation=cms.vdouble(0.0, 1.479, 4.0),
    TrkIsolation=cms.vdouble(99999.0, 99999.0),
    Scalings=cms.PSet(  # for EGPhotonOfflineEtCut, taken from PhaseIIL1TriggerMenuTools twiki
        barrel=cms.vdouble(2.6604, 1.06077, 0.0),
        endcap=cms.vdouble(3.17445, 1.13219, 0.0),
    ),
)

process.L1TkEmDouble24Filter = cms.EDFilter(
    "L1TTkEmFilter",
    saveTags=cms.bool(True),
    MinPt=cms.double(24.0),
    MinN=cms.int32(2),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    inputTag1=cms.InputTag("L1TkPhotonsCrystal", "EG"),
    inputTag2=cms.InputTag("L1TkPhotonsHGC", "EG"),
    Qual1IsMask=cms.bool(True),
    Qual2IsMask=cms.bool(False),
    ApplyQual1=cms.bool(True),
    ApplyQual2=cms.bool(True),
    Quality1=cms.int32(0x2),
    Quality2=cms.int32(5),
    EtaBinsForIsolation=cms.vdouble(0.0, 1.479, 4.0),
    TrkIsolation=cms.vdouble(99999.0, 99999.0),
    Scalings=cms.PSet(  # for EGPhotonOfflineEtCut, taken from PhaseIIL1TriggerMenuTools twiki
        barrel=cms.vdouble(2.6604, 1.06077, 0.0),
        endcap=cms.vdouble(3.17445, 1.13219, 0.0),
    ),
)

process.L1TkEmSingle51Filter = cms.EDFilter(
    "L1TTkEmFilter",
    saveTags=cms.bool(True),
    MinPt=cms.double(51.0),
    MinN=cms.int32(1),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    inputTag1=cms.InputTag("L1TkPhotonsCrystal", "EG"),
    inputTag2=cms.InputTag("L1TkPhotonsHGC", "EG"),
    Qual1IsMask=cms.bool(True),
    Qual2IsMask=cms.bool(False),
    ApplyQual1=cms.bool(True),
    ApplyQual2=cms.bool(True),
    Quality1=cms.int32(0x2),
    Quality2=cms.int32(5),
    EtaBinsForIsolation=cms.vdouble(0.0, 1.479, 4.0),
    TrkIsolation=cms.vdouble(99999.0, 99999.0),
    Scalings=cms.PSet(  # for EGPhotonOfflineEtCut, taken from PhaseIIL1TriggerMenuTools twiki
        barrel=cms.vdouble(2.6604, 1.06077, 0.0),
        endcap=cms.vdouble(3.17445, 1.13219, 0.0),
    ),
)

process.L1TkIsoEleSingle28Filter = cms.EDFilter(
    "L1TTkEleFilter",
    saveTags=cms.bool(True),
    MinPt=cms.double(28.0),
    MinN=cms.int32(1),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    inputTag1=cms.InputTag("L1TkElectronsEllipticMatchCrystal", "EG"),
    inputTag2=cms.InputTag("L1TkElectronsEllipticMatchHGC", "EG"),
    Qual1IsMask=cms.bool(True),
    Qual2IsMask=cms.bool(False),
    ApplyQual1=cms.bool(True),
    ApplyQual2=cms.bool(True),
    Quality1=cms.int32(0x2),
    Quality2=cms.int32(5),
    EtaBinsForIsolation=cms.vdouble(0.0, 1.479, 4.0),
    TrkIsolation=cms.vdouble(0.12, 0.20),
    Scalings=cms.PSet(  # for TkIsoElectronOfflineEtCut, taken from PhaseIIL1TriggerMenuTools twiki
        barrel=cms.vdouble(0.434262, 1.20586, 0.0),
        endcap=cms.vdouble(0.266186, 1.25976, 0.0),
    ),
)

process.L1TkIsoEmDouble12Filter = cms.EDFilter(
    "L1TTkEmFilter",
    saveTags=cms.bool(True),
    MinPt=cms.double(12.0),
    MinN=cms.int32(2),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    inputTag1=cms.InputTag("L1TkPhotonsCrystal", "EG"),
    inputTag2=cms.InputTag("L1TkPhotonsHGC", "EG"),
    Qual1IsMask=cms.bool(True),
    Qual2IsMask=cms.bool(False),
    ApplyQual1=cms.bool(True),
    ApplyQual2=cms.bool(True),
    Quality1=cms.int32(0x2),
    Quality2=cms.int32(5),
    EtaBinsForIsolation=cms.vdouble(0.0, 1.479, 4.0),
    TrkIsolation=cms.vdouble(0.35, 0.28),
    Scalings=cms.PSet(  # for TkIsoPhotonOfflineEtCut, taken from PhaseIIL1TriggerMenuTools twiki
        barrel=cms.vdouble(2.54255, 1.08749, 0.0),
        endcap=cms.vdouble(2.11186, 1.15524, 0.0),
    ),
)

process.L1TkIsoEmSingle22Filter = cms.EDFilter(
    "L1TTkEmFilter",
    saveTags=cms.bool(True),
    MinPt=cms.double(22.0),
    MinN=cms.int32(1),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    inputTag1=cms.InputTag("L1TkPhotonsCrystal", "EG"),
    inputTag2=cms.InputTag("L1TkPhotonsHGC", "EG"),
    Qual1IsMask=cms.bool(True),
    Qual2IsMask=cms.bool(False),
    ApplyQual1=cms.bool(True),
    ApplyQual2=cms.bool(True),
    Quality1=cms.int32(0x2),
    Quality2=cms.int32(5),
    EtaBinsForIsolation=cms.vdouble(0.0, 1.479, 4.0),
    TrkIsolation=cms.vdouble(0.35, 0.28),
    Scalings=cms.PSet(  # for TkIsoPhotonOfflineEtCut, taken from PhaseIIL1TriggerMenuTools twiki
        barrel=cms.vdouble(2.54255, 1.08749, 0.0),
        endcap=cms.vdouble(2.11186, 1.15524, 0.0),
    ),
)
process.L1TkIsoEleSingle22Filter = cms.EDFilter("L1TTkEleFilter",
       saveTags = cms.bool( True ),
       MinPt = cms.double( 22.0 ),
       MinN=cms.int32(1),
       MinEta=cms.double(-2.4),
       MaxEta=cms.double(2.4),
       inputTag1 = cms.InputTag("L1TkElectronsEllipticMatchCrystal","EG"),
       inputTag2 = cms.InputTag("L1TkElectronsEllipticMatchHGC","EG"),
       Qual1IsMask = cms.bool( True ), 
       Qual2IsMask = cms.bool( False ),
       ApplyQual1 = cms.bool( True ),
       ApplyQual2 = cms.bool( True ),
       Quality1 = cms.int32(0x2),
       Quality2 = cms.int32(5),
       EtaBinsForIsolation = cms.vdouble(0.0,1.479,2.4),
       TrkIsolation = cms.vdouble(0.12,0.20),
       Scalings = cms.PSet( # for TkIsoElectronOfflineEtCut, taken from PhaseIIL1TriggerMenuTools twiki
           barrel=cms.vdouble(0.434262,1.20586,0.0),
           endcap=cms.vdouble(0.266186,1.25976,0.0),
       )                             
)

process.L1TkEmDouble12Filter = cms.EDFilter("L1TTkEmFilter",
       saveTags = cms.bool( True ),
       MinPt = cms.double( 12.0 ),
       MinN=cms.int32(2),
       MinEta=cms.double(-2.4), 
       MaxEta=cms.double(2.4),
       inputTag1 = cms.InputTag("L1TkPhotonsCrystal","EG"),
       inputTag2 = cms.InputTag("L1TkPhotonsHGC","EG"),
       Qual1IsMask = cms.bool( True ), 
       Qual2IsMask = cms.bool( False ),
       ApplyQual1 = cms.bool( True ),
       ApplyQual2 = cms.bool( True ),
       Quality1 = cms.int32(0x2),
       Quality2 = cms.int32(5),
       EtaBinsForIsolation = cms.vdouble(0.0,1.479,2.4),
       TrkIsolation = cms.vdouble(99999.0,99999.0),
       Scalings = cms.PSet( # for EGPhotonOfflineEtCut, taken from PhaseIIL1TriggerMenuTools twiki
           barrel=cms.vdouble(2.6604,1.06077,0.0),
           endcap=cms.vdouble(3.17445,1.13219,0.0),
       )                             
)


process.L1TkIsoEmSingle36Filter = cms.EDFilter(
    "L1TTkEmFilter",
    saveTags=cms.bool(True),
    MinPt=cms.double(36.0),
    MinN=cms.int32(1),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    inputTag1=cms.InputTag("L1TkPhotonsCrystal", "EG"),
    inputTag2=cms.InputTag("L1TkPhotonsHGC", "EG"),
    Qual1IsMask=cms.bool(True),
    Qual2IsMask=cms.bool(False),
    ApplyQual1=cms.bool(True),
    ApplyQual2=cms.bool(True),
    Quality1=cms.int32(0x2),
    Quality2=cms.int32(5),
    EtaBinsForIsolation=cms.vdouble(0.0, 1.479, 4.0),
    TrkIsolation=cms.vdouble(0.35, 0.28),
    Scalings=cms.PSet(  # for TkIsoPhotonOfflineEtCut, taken from PhaseIIL1TriggerMenuTools twiki
        barrel=cms.vdouble(2.54255, 1.08749, 0.0),
        endcap=cms.vdouble(2.11186, 1.15524, 0.0),
    ),
)

### Sequences

### THIAGO: NEEDS THE DELTAZ CUT!!!
process.L1TTkEle25TkEle12Sequence = cms.Sequence(
    process.L1TkEleSingle25Filter + process.L1TkEleDouble12Filter
)

process.L1TTkEle36Sequence = cms.Sequence(process.L1TkEleSingle36Filter)

process.L1TTkEm37TkEm24Sequence = cms.Sequence(
    process.L1TkEmSingle37Filter + process.L1TkEmDouble24Filter
)

process.L1TTkEm51Sequence = cms.Sequence(process.L1TkEmSingle51Filter)

process.L1TTkIsoEle28Sequence = cms.Sequence(process.L1TkIsoEleSingle28Filter)

process.L1TTkIsoEm22TkIsoEm12Sequence = cms.Sequence(
    process.L1TkIsoEmSingle22Filter + process.L1TkIsoEmDouble12Filter
)
process.L1TTkIsoEle22TkEm12Sequence = cms.Sequence(
    process.L1TkIsoEleSingle22Filter +
    process.L1TkEmDouble12Filter
)

process.L1TTkIsoEm36Sequence = cms.Sequence(process.L1TkIsoEmSingle36Filter)

### JETMET ###

### Reference: https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/hltPhase2_L1T.py
### Set the L1jets explicitly
from L1Trigger.L1CaloTrigger.Phase1L1TJets_cff import (
    Phase1L1TJetProducer,
    Phase1L1TJetCalibrator,
)

process.l1tSlwPFPuppiJets = Phase1L1TJetProducer.clone(
    inputCollectionTag="l1pfCandidates:Puppi",
    outputCollectionName="UncalibratedPhase1L1TJetFromPfCandidates",
)

process.l1tSlwPFPuppiJetsCorrected = Phase1L1TJetCalibrator.clone(
    inputCollectionTag="l1tSlwPFPuppiJets:UncalibratedPhase1L1TJetFromPfCandidates",
    outputCollectionName="Phase1L1TJetFromPfCandidates",
)

process.l1tReconstructionSeq = cms.Sequence(
    process.l1tSlwPFPuppiJets + process.l1tSlwPFPuppiJetsCorrected
)

process.l1tSinglePFPuppiJet230off = cms.EDFilter(
    "L1TJetFilter",
    inputTag=cms.InputTag("l1tSlwPFPuppiJetsCorrected", "Phase1L1TJetFromPfCandidates"),
    Scalings=cms.PSet(
        barrel=cms.vdouble(11.1254, 1.40627, 0),
        overlap=cms.vdouble(24.8375, 1.4152, 0),
        endcap=cms.vdouble(42.4039, 1.33052, 0),
    ),
    MinPt=cms.double(230.0),
    MinEta=cms.double(-5.0),
    MaxEta=cms.double(5.0),
    MinN=cms.int32(1),
)

process.l1tPFPuppiHT = cms.EDProducer(
    "HLTHtMhtProducer",
    jetsLabel=cms.InputTag(
        "l1tSlwPFPuppiJetsCorrected", "Phase1L1TJetFromPfCandidates"
    ),
    minPtJetHt=cms.double(30.0),
    maxEtaJetHt=cms.double(2.4),
)

process.l1tPFPuppiHT450off = cms.EDFilter(
    "L1TEnergySumFilter",
    inputTag=cms.InputTag("l1tPFPuppiHT"),
    Scalings=cms.PSet(
        theScalings=cms.vdouble(50.0182, 1.0961, 0),  # PFPhase1HT090OfflineEtCut
    ),
    TypeOfSum=cms.string("HT"),
    MinPt=cms.double(450.0),
)

process.l1tPFPuppiMET220off = cms.EDFilter(
    "L1TPFEnergySumFilter",
    inputTag=cms.InputTag("l1PFMetPuppi"),
    Scalings=cms.PSet(
        theScalings=cms.vdouble(54.2859, 1.39739, 0),  # PuppiMET090OfflineEtCut
    ),
    TypeOfSum=cms.string("MET"),
    MinPt=cms.double(220.0),
)

### BTAG ###

### Reference: https://github.com/johnalison/RecoBTag-PerformanceMeasurements/blob/PhaseIIOnline/python/Configs/testTriggerPaths_cfg.py
### We use the L1jets explicitly set by JetMET

process.l1tPFPuppiHTMaxEta2p4 = cms.EDProducer(
    "HLTHtMhtProducer",
    jetsLabel=cms.InputTag(
        "l1tSlwPFPuppiJetsCorrected", "Phase1L1TJetFromPfCandidates"
    ),
    minPtJetHt=cms.double(30.0),
    maxEtaJetHt=cms.double(2.4),
)

process.l1tPFPuppiHT400offMaxEta2p4 = cms.EDFilter(
    "L1TEnergySumFilter",
    inputTag=cms.InputTag("l1tPFPuppiHTMaxEta2p4"),
    Scalings=cms.PSet(
        theScalings=cms.vdouble(50.0182, 1.0961, 0),  # PFPhase1HT090OfflineEtCut
    ),
    TypeOfSum=cms.string("HT"),
    MinPt=cms.double(400.0),
)

process.l1t1PFPuppiJet70offMaxEta2p4 = cms.EDFilter(
    "L1TJetFilter",
    inputTag=cms.InputTag("l1tSlwPFPuppiJetsCorrected", "Phase1L1TJetFromPfCandidates"),
    Scalings=cms.PSet(
        barrel=cms.vdouble(11.1254, 1.40627, 0),
        overlap=cms.vdouble(24.8375, 1.4152, 0),
        endcap=cms.vdouble(42.4039, 1.33052, 0),
    ),
    MinPt=cms.double(70.0),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    MinN=cms.int32(1),
)

process.l1t2PFPuppiJet55offMaxEta2p4 = cms.EDFilter(
    "L1TJetFilter",
    inputTag=cms.InputTag("l1tSlwPFPuppiJetsCorrected", "Phase1L1TJetFromPfCandidates"),
    Scalings=cms.PSet(
        barrel=cms.vdouble(11.1254, 1.40627, 0),
        overlap=cms.vdouble(24.8375, 1.4152, 0),
        endcap=cms.vdouble(42.4039, 1.33052, 0),
    ),
    MinPt=cms.double(55.0),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    MinN=cms.int32(2),
)

process.l1t4PFPuppiJet40offMaxEta2p4 = cms.EDFilter(
    "L1TJetFilter",
    inputTag=cms.InputTag("l1tSlwPFPuppiJetsCorrected", "Phase1L1TJetFromPfCandidates"),
    Scalings=cms.PSet(
        barrel=cms.vdouble(11.1254, 1.40627, 0),
        overlap=cms.vdouble(24.8375, 1.4152, 0),
        endcap=cms.vdouble(42.4039, 1.33052, 0),
    ),
    MinPt=cms.double(40.0),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    MinN=cms.int32(4),
)

process.l1t4PFPuppiJet25OnlineMaxEta2p4 = cms.EDFilter(
    "L1TJetFilter",
    inputTag=cms.InputTag("l1tSlwPFPuppiJetsCorrected", "Phase1L1TJetFromPfCandidates"),
    # Scalings = cms.PSet( ## no scaling
    #   barrel = cms.vdouble(11.1254, 1.40627, 0),
    #   overlap = cms.vdouble(24.8375, 1.4152, 0),
    #   endcap = cms.vdouble(42.4039, 1.33052, 0),
    # ),
    MinPt=cms.double(25.0),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    MinN=cms.int32(4),
)

process.l1tDoublePFPuppiJet112offMaxEta2p4 = cms.EDFilter(
    "L1TJetFilter",
    inputTag=cms.InputTag("l1tSlwPFPuppiJetsCorrected", "Phase1L1TJetFromPfCandidates"),
    Scalings=cms.PSet(
        barrel=cms.vdouble(11.1254, 1.40627, 0),
        overlap=cms.vdouble(24.8375, 1.4152, 0),
        endcap=cms.vdouble(42.4039, 1.33052, 0),
    ),
    MinPt=cms.double(112.0),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    MinN=cms.int32(2),
    saveTags=cms.bool(True),
)

process.l1tDoublePFPuppiJets112offMaxDeta1p6 = cms.EDFilter(
    "HLT2CaloJetCaloJet",
    saveTags=cms.bool(True),
    MinMinv=cms.double(0.0),
    originTag2=cms.VInputTag(
        "l1tSlwPFPuppiJetsCorrected::Phase1L1TJetFromPfCandidates"
    ),
    MinDelR=cms.double(0.0),
    MinPt=cms.double(0.0),
    MinN=cms.int32(1),
    originTag1=cms.VInputTag(
        "l1tSlwPFPuppiJetsCorrected::Phase1L1TJetFromPfCandidates"
    ),
    triggerType1=cms.int32(-116),
    triggerType2=cms.int32(-116),
    MaxMinv=cms.double(1.0e7),
    MinDeta=cms.double(-1000.0),
    MaxDelR=cms.double(1000.0),
    inputTag1=cms.InputTag("l1tDoublePFPuppiJet112offMaxEta2p4"),
    inputTag2=cms.InputTag("l1tDoublePFPuppiJet112offMaxEta2p4"),
    MaxDphi=cms.double(1.0e7),
    MaxDeta=cms.double(1.6),
    MaxPt=cms.double(1.0e7),
    MinDphi=cms.double(0.0),
)

### Taus ###


if options.runL1HPSTaus:
    process.HLTL1TauSequence = cms.Sequence(process.HLTL1Sequence)
    
    from L1Trigger.Phase2L1Taus.HPSPFTauProducerPF_cfi import HPSPFTauProducerPF
    from L1Trigger.Phase2L1Taus.HPSPFTauProducerPuppi_cfi import HPSPFTauProducerPuppi
    for useStrips in [ True, False ]:
        for applyPreselection in [ True, False ]:
            moduleNameBase = "HPSPFTauProducer"
            if useStrips and applyPreselection:
                moduleNameBase += "WithStripsAndPreselection"
            elif useStrips and not applyPreselection:
                moduleNameBase += "WithStripsWithoutPreselection"
            elif not useStrips and applyPreselection:
                moduleNameBase += "WithoutStripsWithPreselection"
            elif not useStrips and not applyPreselection:
                moduleNameBase += "WithoutStripsAndPreselection"
            else:
                raise ValueError("Invalid Combination of 'useStrips' and 'applyPreselection' Configuration parameters !!")
        
            moduleNamePF = moduleNameBase + "PF"
            modulePF = HPSPFTauProducerPF.clone(
                useStrips = cms.bool(useStrips),
                applyPreselection = cms.bool(applyPreselection),
                debug = cms.untracked.bool(False)
            )
            setattr(process, moduleNamePF, modulePF)
            process.HLTL1TauSequence += getattr(process, moduleNamePF)

            moduleNamePuppi = moduleNameBase + "Puppi"
            modulePuppi = HPSPFTauProducerPuppi.clone(
                useStrips = cms.bool(useStrips),
                applyPreselection = cms.bool(applyPreselection),
                debug = cms.untracked.bool(False)
            )
            setattr(process, moduleNamePuppi, modulePuppi)
            process.HLTL1TauSequence += getattr(process, moduleNamePuppi)
            

 
    #https://indico.cern.ch/event/1017753/contributions/4271145/attachments/2209533/3739186/Sandeep_Phase2_L1_TauTrigger_20210316_v1.pdf
    process.hltL1DoubleHPSTau21 = cms.EDFilter("L1THPSPFTauFilter",
                                               MaxEta=cms.double(2.1),
                                               MinEta=cms.double(-2.1),
                                               MinN=cms.int32(2),
                                               MinPt=cms.double(21.0),
                                               MaxRelChargedIso = cms.double(0.05),
                                               MinLeadTrackPt = cms.double(5),
                                               inputTag=cms.InputTag("HPSPFTauProducerWithStripsWithoutPreselectionPF", "", "L1TSkimming"),
                                               saveTags=cms.bool(True),
                                           )

    process.hltL1DoubleHPSTau21DZ = cms.EDFilter(
        "HLT2L1HPSPFTauL1HPSPFTauDZ",
        MaxDZ=cms.double(0.4),
        MinDR=cms.double(0.5),
        MinN=cms.int32(1),
        MinPixHitsForDZ=cms.int32(0),
        checkSC=cms.bool(False),
        inputTag1=cms.InputTag("hltL1DoubleHPSTau21"),
        inputTag2=cms.InputTag("hltL1DoubleHPSTau21"),
        originTag1=cms.VInputTag("HPSPFTauProducerWithStripsWithoutPreselectionPF::L1TSkimming"),
        originTag2=cms.VInputTag("HPSPFTauProducerWithStripsWithoutPreselectionPF::L1TSkimming"),
        saveTags=cms.bool(True),
        triggerType1=cms.int32(-117),
        triggerType2=cms.int32(-117),
    )


    process.hltL1SingleHPSTau52 = cms.EDFilter("L1THPSPFTauFilter",
                                               MaxEta=cms.double(2.172),
                                               MinEta=cms.double(-2.172),
                                               MinN=cms.int32(1),
                                               MinPt=cms.double(52.0),
                                               MaxRelChargedIso = cms.double(0.05),
                                               MinLeadTrackPt = cms.double(5),
                                               inputTag=cms.InputTag("HPSPFTauProducerWithStripsWithoutPreselectionPF", "", "L1TSkimming"),
                                               saveTags=cms.bool(True),
                                           )

process.hltL1DoubleNNTau52 = cms.EDFilter("L1TPFTauFilter",
                                          MaxEta=cms.double(2.172),
                                          MinEta=cms.double(-2.172),
                                          MinN=cms.int32(2),
                                          MinPt=cms.double(52.0),
                                          PassLooseNN = cms.int32(0),
                                          inputTag=cms.InputTag("l1NNTauProducerPuppi", "L1PFTausNN", "L1TSkimming"),
                                          Scalings = cms.PSet(
                                              barrel=cms.vdouble(-9.54135, 1.73403, 0),
                                              endcap=cms.vdouble(-36.157, 3.83749, 0),
                                          ),
                                          saveTags=cms.bool(True),
                                       )
process.hltL1SingleNNTau150 = cms.EDFilter("L1TPFTauFilter",
                                           MaxEta=cms.double(2.172),
                                           MinEta=cms.double(-2.172),
                                           MinN=cms.int32(1),
                                           MinPt=cms.double(150.0),
                                           PassLooseNN = cms.int32(0),
                                           inputTag=cms.InputTag("l1NNTauProducerPuppi", "L1PFTausNN", "L1TSkimming"),
                                           Scalings = cms.PSet(
                                               barrel=cms.vdouble(-9.54135, 1.73403, 0),
                                               endcap=cms.vdouble(-36.157, 3.83749, 0),
                                           ),
                                           saveTags=cms.bool(True),
                                      )


### PATHS ###
process.HLTL1TPath = cms.Path(process.HLTL1Sequence)

### Paths with the same name as the original Muons
### EXCEPT I changed "L1_" to "L1T_"
process.L1T_SingleTkMuon_22 = cms.Path(
    process.HLTL1Sequence + process.hltL1TkSingleMuFiltered22
)
# This path was mistakenly named "L1_DoubleTkMuon_17_8"
process.L1T_DoubleTkMuon_15_7 = cms.Path(
    process.HLTL1Sequence
    + process.hltL1TkDoubleMuFiltered7
    + process.hltL1TkSingleMuFiltered15
    + process.hltDoubleMuon7DZ1p0
)
process.L1T_TripleTkMuon_5_3_3 = cms.Path(
    process.HLTL1Sequence
    + process.hltL1TripleMuFiltered3
    + process.hltL1SingleMuFiltered5
    + process.hltTripleMuon3DZ1p0
    + process.hltTripleMuon3DR0
)

### Paths with the same name as the original EGamma
process.L1T_TkEle36 = cms.Path(process.HLTL1Sequence + process.L1TTkEle36Sequence)
process.L1T_TkIsoEle28 = cms.Path(process.HLTL1Sequence + process.L1TTkIsoEle28Sequence)
process.L1T_TkEle25TkEle12 = cms.Path(
    process.HLTL1Sequence + process.L1TTkEle25TkEle12Sequence
)
process.L1T_TkIsoEle22TkEm12 = cms.Path(
    process.HLTL1Sequence+
    process.L1TTkIsoEle22TkEm12Sequence 
)

process.L1T_TkEm51 = cms.Path(process.HLTL1Sequence + process.L1TTkEm51Sequence)
process.L1T_TkEm37TkEm24 = cms.Path(
    process.HLTL1Sequence + process.L1TTkEm37TkEm24Sequence
)
process.L1T_TkIsoEm36 = cms.Path(process.HLTL1Sequence + process.L1TTkIsoEm36Sequence)
process.L1T_TkIsoEm22TkIsoEm12 = cms.Path(
    process.HLTL1Sequence + process.L1TTkIsoEm22TkIsoEm12Sequence
)

### Paths with the same name as original JME
process.L1T_SinglePFPuppiJet230off = cms.Path(
    process.HLTL1Sequence
    + process.l1tReconstructionSeq
    + process.l1tSinglePFPuppiJet230off
)
process.L1T_PFPuppiMET220off = cms.Path(
    process.HLTL1Sequence + process.l1tPFPuppiMET220off
)
process.L1T_PFPuppiHT450off = cms.Path(
    process.HLTL1Sequence
    + process.l1tReconstructionSeq
    + process.l1tPFPuppiHT
    + process.l1tPFPuppiHT450off
)

### Paths NOT with the same name as original BTV
### (Made changes to accurately reflect path)
### Also: renamed "L1_" to "L1T_"
process.L1T_PFHT400PT30_QuadPFPuppiJet_70_55_40_40_2p4 = cms.Path(
    process.HLTL1Sequence
    + process.l1tReconstructionSeq
    + process.l1tPFPuppiHTMaxEta2p4
    + process.l1tPFPuppiHT400offMaxEta2p4
    + process.l1t1PFPuppiJet70offMaxEta2p4
    + process.l1t2PFPuppiJet55offMaxEta2p4
    + process.l1t4PFPuppiJet40offMaxEta2p4
    + process.l1t4PFPuppiJet25OnlineMaxEta2p4
)

process.L1T_DoublePFPuppiJets112_2p4_DEta1p6 = cms.Path(
    process.HLTL1Sequence
    + process.l1tReconstructionSeq
    + process.l1tDoublePFPuppiJet112offMaxEta2p4
    + process.l1tDoublePFPuppiJets112offMaxDeta1p6
)

if options.runL1NNTaus:
    process.L1T_DoubleNNTau52 = cms.Path(
        process.HLTL1Sequence +
        process.hltL1DoubleNNTau52
    )
 #   process.L1T_SingleNNTau150 = cms.Path(
 #       process.HLTL1Sequence +
 #       process.hltL1SingleNNTau150
 #   )

if options.runL1HPSTaus:
    process.L1T_DoubleHPSTau21 = cms.Path(
        process.HLTL1TauSequence +
        process.hltL1DoubleHPSTau21 + 
        process.hltL1DoubleHPSTau21DZ
    )
  #  process.L1T_SingleHPSTau52 = cms.Path(
  #      process.HLTL1TauSequence +
  #      process.hltL1SingleHPSTau52
  #  )
        

### Aging
from SLHCUpgradeSimulations.Configuration.aging import customise_aging_1000

customise_aging_1000(process)

eghlt_tools.customiseMessageLogger(process,reportEvery=20)

### Output
process.hltOutputTot = cms.OutputModule(
    "PoolOutputModule",
    fileName=cms.untracked.string(options.outputFile),
    SelectEvents=cms.untracked.PSet(SelectEvents=cms.vstring()),
    outputCommands = cms.untracked.vstring()
)

process.hltOutputTot.SelectEvents.SelectEvents = cms.vstring()

eventContentL1 = cms.untracked.vstring(
    'keep *_l1EGammaEEProducer_*_*',
    'keep *_L1EGammaClusterEmuProducer_*_*',
    'keep *_L1TkPhotonsHGC_*_*',
    'keep *_L1TkPhotonsCrystal_*_*',
    'keep *_L1TkElectronsEllipticMatchCrystal_*_*',
    'keep *_L1TkElectronsEllipticMatchHGC_*_*',
    'keep *_L1TkMuons_*_*',
    'keep *_l1tSlwPFPuppiJetsCorrected_*_*',
    'keep *_l1tPFPuppiHT_*_*',
    'keep *_l1PFMetPuppi_*_*',
    'keep *_l1tPFPuppiHTMaxEta2p4_*_*',
    'keep *_TTTracksFromTrackletEmulation_Level1TTTracks_*',
    'keep *_l1pf*Candidates_*_*',
    'keep *_HPSPFTauProducerWithStripsWithoutPreselectionPF_*_*',
    'keep *_*_*_L1TSkimming',
    )
eventContentL1Only = cms.untracked.vstring(
    'drop *',
    )
eventContentL1Only.extend(eventContentL1)


eventContentReduced = cms.untracked.vstring(   
    'keep *_*_*_SIM',
    'keep *_*_*_HLT',    
    'drop *_*_*_RECO',
    'drop *_*_*_L1',
    'drop simEcalEBTriggerPrimitiveDigis_*_*_*',
    'drop TrackingParticles_mix_MergedTrackTruth_HLT',
    'drop TrackingVertexs_mix_MergedTrackTruth_HLT',
    'drop TrackingVertexs_mix_InitialVertices_HLT',
    #'drop CaloParticles_mix_MergedCaloTruth_HLT',
    'drop PCaloHits_g4SimHits_EcalHitsEB_SIM',
    'drop PCaloHits_g4SimHits_HGCHitsEE_SIM',
    #'drop SimClusters_mix_MergedCaloTruth_HLT',
    'drop *_me0RecHits_*_*',

)
eventContentReduced.extend(eventContentL1)
   
if options.reducedEvt:
    process.hltOutputTot.outputCommands = eventContentReduced
if options.l1OnlyEvt:
    process.hltOutputTot.outputCommands = eventContentL1Only

for pathname in process.pathNames().split():
    if pathname.startswith("L1T_"):
        process.hltOutputTot.SelectEvents.SelectEvents.append(pathname)

process.outPath = cms.EndPath(process.hltOutputTot)

### SCHEDULE ###
process.schedule = cms.Schedule(
    *[
        process.HLTL1TPath,
        process.L1T_SingleTkMuon_22,
        process.L1T_DoubleTkMuon_15_7,
        process.L1T_TripleTkMuon_5_3_3,
        process.L1T_TkEle36,
        process.L1T_TkIsoEle28,
        process.L1T_TkEle25TkEle12,
        process.L1T_TkEm51,
        process.L1T_TkEm37TkEm24,
        process.L1T_TkIsoEm36,
        process.L1T_TkIsoEle22TkEm12,
        process.L1T_TkIsoEm22TkIsoEm12,
        process.L1T_SinglePFPuppiJet230off,
        process.L1T_PFPuppiMET220off,
        process.L1T_PFPuppiHT450off,
        process.L1T_PFHT400PT30_QuadPFPuppiJet_70_55_40_40_2p4,
        process.L1T_DoublePFPuppiJets112_2p4_DEta1p6,
      
        process.outPath,
    ]
)
if options.runL1HPSTaus:
    process.schedule.append(process.L1T_DoubleHPSTau21 )
#    process.schedule.append(process.L1T_SingleHPSTau52 )

if options.runL1NNTaus:
    process.schedule.append(process.L1T_DoubleNNTau52)
#    process.schedule.append(process.L1T_SingleNNTau150)
    
if options.runOnExisting:
    process.HLTL1Sequence = cms.Sequence()
    process.HLTL1TauSequence = cms.Sequence()

    process.hltL1DoubleHPSTau21.inputTag=cms.InputTag("L1HPSPFTauProducerWithStripsPF", "", "L1TSkimming")
    process.hltL1DoubleHPSTau21DZ.originTag1 = cms.VInputTag("L1HPSPFTauProducerWithStripsPF::L1TSkimming")
    process.hltL1DoubleHPSTau21DZ.originTag2 = cms.VInputTag("L1HPSPFTauProducerWithStripsPF::L1TSkimming")
    process.hltL1SingleHPSTau52.inputTag=cms.InputTag("L1HPSPFTauProducerWithStripsPF", "", "L1TSkimming")

print "eventcontent:"
print process.hltOutputTot.outputCommands.value()
print "filter paths:"
print process.hltOutputTot.SelectEvents.SelectEvents.value()
print "global tag:",process.GlobalTag.globaltag.value()
