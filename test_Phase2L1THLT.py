import FWCore.ParameterSet.Config as cms

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
    input=cms.untracked.int32(2849),
    output=cms.optional.untracked.allowed(cms.int32, cms.PSet),
)

process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))

### Input source
process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/E60846B8-DAFC-E347-954A-99B926A15310.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/E64B49BC-1C1E-B248-8301-BFECE2318AFA.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/E66C842A-081D-FC44-AAE7-436CB64BEDEA.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/E724F136-35D0-D549-8409-70E88D9C2F53.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/E7B29780-A1C8-5241-8050-79DACDAA6425.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/E7EEF490-ACD8-DD4E-86E4-1190990136AD.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/E804EB3A-5F40-A949-8283-1427ACCC7229.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/E8187E32-9379-7444-B910-867E2DB709DA.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/E8448DF4-4717-F74D-A3DD-3F580280951D.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/E8CE39AA-0AAF-8744-8CDA-E1DA9DD18F81.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/FBC3DC30-72C0-9442-9E6A-DFC89D38DE0C.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/FBE51CD4-E125-F347-900D-25D780323C00.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/FC6EDB5C-160D-E14B-B0F7-B34A15A8649A.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/FC78AF20-8C11-8E4D-A2D2-9011278E1DCF.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/FCE2A878-D3BB-4E44-A274-63FDA61D6C0A.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/FD2C7F36-5BEF-8645-8F73-3B645C45F986.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/FF2DB685-2ABB-1545-9F5A-754AABF28F96.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/FF661451-502A-FC47-A868-A9F2071874CB.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/FFA7BAAE-A081-C147-8FA3-5869DD659033.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/FFB0B020-7606-3B46-AB92-23A357884F6C.root",
        # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/120000/FFB3F470-61B4-4545-985C-AE91A6DF4BE3.root",
        # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v2/280000/015FB6F1-59B4-304C-B540-2392A983A97D.root"
        # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FF7BF0E2-1380-2D48-BB19-F79E6907CD5D.root",
        # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/SingleElectron_PT2to200/FEVT/PU200_111X_mcRun4_realistic_T15_v1_ext2-v1/270000/0064D31F-F48B-3144-8CB9-17F820065E01.root",
    ),
)

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
        process.L1T_TkIsoEm22TkIsoEm12,
        process.L1T_SinglePFPuppiJet230off,
        process.L1T_PFPuppiMET220off,
        process.L1T_PFPuppiHT450off,
    ]
)

### Aging
from SLHCUpgradeSimulations.Configuration.aging import customise_aging_1000

customise_aging_1000(process)
