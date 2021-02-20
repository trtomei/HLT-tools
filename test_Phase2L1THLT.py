import FWCore.ParameterSet.Config as cms

process = cms.Process("L1TSkimming")

process.load("Configuration.StandardSequences.Services_cff")
process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet(
    input=cms.untracked.int32(-1),
    output=cms.optional.untracked.allowed(cms.int32, cms.PSet),
)

process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))

### Input source
process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/120000/FFB3F470-61B4-4545-985C-AE91A6DF4BE3.root",
        #"/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v2/280000/015FB6F1-59B4-304C-B540-2392A983A97D.root"
        #"/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FF7BF0E2-1380-2D48-BB19-F79E6907CD5D.root",
        # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/SingleElectron_PT2to200/FEVT/PU200_111X_mcRun4_realistic_T15_v1_ext2-v1/270000/0064D31F-F48B-3144-8CB9-17F820065E01.root",
    ),
)

### GlobalTag
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag

process.GlobalTag = GlobalTag(process.GlobalTag, "111X_mcRun4_realistic_T15_v4", "")

### MUON ###

process.l1tMuon22 = cms.EDFilter(
    "L1TTkMuonFilter",
    MinPt=cms.double(22.0),
    MinN=cms.int32(1),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    inputTag=cms.InputTag("L1TkMuons"),
    Scalings=cms.PSet(
        barrel=cms.vdouble(0.802461, 1.04193, 0.0),
        overlap=cms.vdouble(0.921315, 1.03611, 0.0),
        endcap=cms.vdouble(0.828802, 1.03447, 0.0),
    ),
)

process.l1tTkMu15 = process.l1tMuon22.clone(
    MinPt=15.0,
)

process.l1tTkMu7TkMu7 = process.l1tMuon22.clone(
    MinPt=7.0,
    MinN=2,
)

process.l1tTkMu15TkMu7DZ1p0 = cms.EDFilter(
    "HLT2L1TkMuonL1TkMuonDZ",
    originTag1=cms.VInputTag(
        "L1TkMuons",
    ),
    originTag2=cms.VInputTag(
        "L1TkMuons",
    ),
    inputTag1=cms.InputTag("l1tTkMu15"),
    inputTag2=cms.InputTag("l1tTkMu7TkMu7"),
    triggerType1=cms.int32(-114),  # L1TkMuon
    triggerType2=cms.int32(-114),  # L1TkMuon
    MinDR=cms.double(-1),
    MaxDZ=cms.double(1.0),
    MinPixHitsForDZ=cms.int32(0),  # Immaterial
    checkSC=cms.bool(False),  # Immaterial
    MinN=cms.int32(1),
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
    TrkIsolation=cms.vdouble(0.28, 0.35),
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
    TrkIsolation=cms.vdouble(0.28, 0.35),
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
    TrkIsolation=cms.vdouble(0.28, 0.35),
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

process.L1T_TkMu22 = cms.Path(process.l1tMuon22)
process.L1T_TkMu15TkMu7DZ1p0 = cms.Path(
    process.l1tTkMu15 + process.l1tTkMu7TkMu7 + process.l1tTkMu15TkMu7DZ1p0
)
# process.L1T_TkMu5TkMu3TkMu3 - cms.Path()

### Paths with the same name as the original EGamma
process.L1T_TkEle36 = cms.Path(process.L1TTkEle36Sequence)
process.L1T_TkIsoEle28 = cms.Path(process.L1TTkIsoEle28Sequence)
process.L1T_TkEle25TkEle12 = cms.Path(process.L1TTkEle25TkEle12Sequence)
process.L1T_TkEm51 = cms.Path(process.L1TTkEm51Sequence)
process.L1T_TkEm37TkEm24 = cms.Path(process.L1TTkEm37TkEm24Sequence)
process.L1T_TkIsoEm36 = cms.Path(process.L1TTkIsoEm36Sequence)
process.L1T_TkIsoEm22TkIsoEm12 = cms.Path(process.L1TTkIsoEm22TkIsoEm12Sequence)

### Paths with the same name as original JME
process.L1T_SinglePFPuppiJet230off = cms.Path(
    process.l1tReconstructionSeq + process.l1tSinglePFPuppiJet230off
)
process.L1T_PFPuppiMET220off = cms.Path(process.l1tPFPuppiMET220off)
process.L1T_PFPuppiHT450off = cms.Path(
    process.l1tReconstructionSeq + process.l1tPFPuppiHT + process.l1tPFPuppiHT450off
)
