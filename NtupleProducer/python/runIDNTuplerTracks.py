import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

process = cms.Process("ID", eras.Phase2C9)

process.load('Configuration.StandardSequences.Services_cff')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000))
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:inputs110X.root'),
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
)

process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '111X_mcRun4_realistic_Candidate_2020_12_09_15_46_46', '')

process.genParticlesCharged = cms.EDFilter("GenParticleSelector", src = cms.InputTag("genParticles"), cut = cms.string("status == 1 && charge != 0"))

from L1Trigger.Phase2L1ParticleFlow.l1ParticleFlow_cff import pfTracksFromL1TracksHGCal, pfTracksFromL1TracksBarrel
process.pfTracksFromL1TracksHGCal = pfTracksFromL1TracksHGCal.clone()
process.pfTracksFromL1TracksBarrel = pfTracksFromL1TracksBarrel.clone()

#to use the extended track collection
process.pfTracksFromL1TracksHGCal.L1TrackTag = cms.InputTag("TTTracksFromExtendedTrackletEmulation", "Level1TTTracks")
process.pfTracksFromL1TracksHGCal.nParam = cms.uint32(5)
process.pfTracksFromL1TracksBarrel.L1TrackTag = cms.InputTag("TTTracksFromExtendedTrackletEmulation", "Level1TTTracks")
process.pfTracksFromL1TracksBarrel.nParam = cms.uint32(5)

ntuple = cms.EDAnalyzer("IDNTuplizer",
                        src = cms.InputTag("pfTracksFromL1TracksHGCal"),
                        #src = cms.InputTag("pfTracksFromL1TracksBarrel"),
                        cut = cms.string("pt > 1"),
                        genParticles = cms.InputTag("genParticlesCharged"),
                        propagateToCalo = cms.bool(True),
                        drMax = cms.double(0.1),
                        minRecoPtOverGenPt = cms.double(0.3),
                        onlyMatched = cms.bool(True),
                        variables = cms.PSet(
                            pt = cms.string("pt"),
                            eta = cms.string("eta"),
                            phi = cms.string("phi"),
                            caloEta = cms.string("caloEta"),
                            caloPhi = cms.string("caloPhi"),
                            trkPtError = cms.string("trkPtError"),
                            caloPtError = cms.string("caloPtError"),
                            isMuon = cms.string("isMuon"),
                            quality = cms.string("quality"),
                            nPar = cms.string("nPar"),
                            nStubs = cms.string("nStubs"),
                            normalizedChi2 = cms.string("normalizedChi2"),
                            chi2 = cms.string("chi2"),

                            #from DataFormats/L1TrackTrigger/interface/TTTrack_TrackWord.h
                            trkWrd_valid = cms.string("trackWord().getValid()"),
                            trkWrd_rinv = cms.string("trackWord().getRinv()"),
                            trkWrd_phi = cms.string("trackWord().getPhi()"),
                            trkWrd_tanl = cms.string("trackWord().getTanl()"),
                            trkWrd_z0 = cms.string("trackWord().getZ0()"),
                            trkWrd_d0 = cms.string("trackWord().getD0()"),
                            trkWrd_chi2RPhi = cms.string("trackWord().getChi2RPhi()"),
                            trkWrd_chi2RZ = cms.string("trackWord().getChi2RZ()"),
                            trkWrd_bendChi2 = cms.string("trackWord().getBendChi2()"),
                            trkWrd_hitPattern = cms.string("trackWord().getHitPattern()"),
                            trkWrd_mvaQuality = cms.string("trackWord().getMVAQuality()"),
                            trkWrd_mvaOther = cms.string("trackWord().getMVAOther()"),
                        ),
                    )
process.ntuple = ntuple.clone()

def newClustering(postfix,
        concentratorAlgo="thresholdSelect", # 'thresholdSelect' or 'superTriggerCellSelect'
        concentratorThreshold=2,
        layer1Algo="dummyC2d",
        layer1Threshold=0,
        layer2Algo="HistoMaxC3d",
        layer2Threshold=0,
        layer2dR=0.03,
        reuseConc=None, reuseL1=None):
    global modules
    if reuseConc is None:
        conc = process.hgcalConcentratorProducer.clone()
        conc.ProcessorParameters.Method = concentratorAlgo
        conc.ProcessorParameters.triggercell_threshold_silicon = concentratorThreshold
        if concentratorThreshold == 0: conc.ProcessorParameters.TCThreshold_fC = 0
        setattr(process, "hgcalConcentratorProducer"+postfix, conc)
        reuseConc = postfix
        modules.append(conc)
    #
    if reuseL1 is None:
        bel1 = process.hgcalBackEndLayer1Producer.clone()
        bel1.InputTriggerCells = cms.InputTag("hgcalConcentratorProducer"+reuseConc,"HGCalConcentratorProcessorSelection")
        bel1.ProcessorParameters.C2d_parameters.clusterType = cms.string(layer1Algo)
        bel1.ProcessorParameters.C2d_parameters.threshold_scintillator = cms.double(layer1Threshold)
        bel1.ProcessorParameters.C2d_parameters.threshold_silicon      = cms.double(layer1Threshold)
        setattr(process, "hgcalBackEndLayer1Producer"+postfix, bel1)
        modules.append(bel1)
        reuseL1 = postfix
    #
    bel2 = process.hgcalBackEndLayer2Producer.clone()
    bel2.InputCluster = cms.InputTag("hgcalBackEndLayer1Producer"+reuseL1,"HGCalBackendLayer1Processor2DClustering")
    bel2.ProcessorParameters.C3d_parameters.type_multicluster = layer2Algo
    bel2.ProcessorParameters.C3d_parameters.threshold_histo_multicluster = layer2Threshold
    if type(layer2dR) == list:
        bel2.ProcessorParameters.C3d_parameters.dR_multicluster_byLayer = cms.vdouble(layer2dR)
        bel2.ProcessorParameters.C3d_parameters.dR_multicluster = 0.03 if type(layer2dR) == list else layer2dR
    else:
        bel2.ProcessorParameters.C3d_parameters.dR_multicluster = 0.03 if type(layer2dR) == list else layer2dR
    setattr(process, "hgcalBackEndLayer2Producer"+postfix, bel2)
    modules.append(bel2)
    #
    nt = ntuple.clone()
    nt.src = cms.InputTag("hgcalBackEndLayer2Producer"+postfix,"HGCalBackendLayer2Processor3DClustering")
    setattr(process, "ntuple"+postfix, nt)
    modules.append(nt)


modules = [
    process.genParticlesCharged,
    process.pfTracksFromL1TracksHGCal,
    process.pfTracksFromL1TracksBarrel,
    process.ntuple
]


process.p = cms.Path(sum(modules[1:], modules[0]))
process.TFileService = cms.Service("TFileService", fileName = cms.string("idTuple.root"))

def goRandom():
    for aname in process.analyzers_().keys():
        if aname.startswith("ntuple"):
            ana = getattr(process,aname)
            if hasattr(ana, 'onlyMatched'):
                ana.onlyMatched = False
def hgcAcc(pdgId,ptmin=2):
    process.acceptance = cms.EDFilter("GenParticleSelector",
        src = cms.InputTag("genParticles"),
        cut = cms.string("abs(pdgId) == %d && pt > %g && abs(eta) > 1.6 && abs(eta) < 2.6" % (pdgId,ptmin)),
        filter = cms.bool(True),
    )
    process.p.insert(0, process.acceptance)
def xdup():
    process.options.numberOfThreads = cms.untracked.uint32(2)
    process.options.numberOfStreams = cms.untracked.uint32(0)


