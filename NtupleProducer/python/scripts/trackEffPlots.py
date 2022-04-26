#python3 trackEffPlots.py
import os
os.system('mkdir -p plots')

from ROOT import TFile, gROOT, gStyle, gDirectory, TStyle, TH1F, TH2F, TCanvas, TString, TLegend, TLegendEntry, TIter, TKey, TPaveLabel, gPad, TGraphAsymmErrors, TEfficiency, THStack

gROOT.SetBatch()
gStyle.SetOptStat(0)
gStyle.SetCanvasBorderMode(0)
gStyle.SetPadBorderMode(0)
gStyle.SetPadColor(0)
gStyle.SetCanvasColor(0)
gStyle.SetTextFont(42)
gStyle.SetCanvasDefH(600)
gStyle.SetCanvasDefW(600)
gStyle.SetCanvasDefX(0)
gStyle.SetCanvasDefY(0)
gStyle.SetPadTopMargin(0.07)
gStyle.SetPadBottomMargin(0.13)
gStyle.SetPadLeftMargin(0.15)
gStyle.SetPadRightMargin(0.05)
gStyle.SetTitleColor(1, "XYZ")
gStyle.SetTitleFont(42, "XYZ")
gStyle.SetTitleSize(0.04, "XYZ")
gStyle.SetTitleXOffset(1.1)
gStyle.SetTextAlign(12)
gStyle.SetLabelColor(1, "XYZ")
gStyle.SetLabelFont(42, "XYZ")
gStyle.SetLabelOffset(0.007, "XYZ")
gStyle.SetLabelSize(0.04, "XYZ")
gStyle.SetAxisColor(1, "XYZ")
gStyle.SetStripDecimals(True)
gStyle.SetTickLength(0.03, "XYZ")
gStyle.SetNdivisions(510, "XYZ")
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)
gROOT.ForceStyle()


def fillHistos(inputFile,variables,hVars,hPtVars):
    if(inputFile.IsZombie()):
        print("input file is zombie")
        sys.exit(1)
    inputFile.cd()
    keys = []
    for key in inputFile.GetListOfKeys():
        keys.append(key.GetName())
        if (key.GetClassName() != "TDirectoryFile"):
            print("no TDirectoryFile")
            sys.exit(1)
    if not "ntuple" in keys:
        print("no Tree, exiting")
        sys.exit(1)
    tree = inputFile.Get("ntuple/tree")

    #loop over tree, fill histograms
    for iEntry in tree:
        for variable,hVar in zip(variables,hVars):
            var = getattr(iEntry, variable)
            hVar.Fill(var)
        
        pt = getattr(iEntry, "pt")
        quality = getattr(iEntry, "quality")
        nStubs = getattr(iEntry, "nStubs")
        normalizedChi2 = getattr(iEntry, "normalizedChi2")

        if quality==1:
            #print("pt is: "+str(pt))
            hPtVars[0].Fill(pt)
        elif quality==3:
            hPtVars[1].Fill(pt)        
        elif quality==4:
            hPtVars[2].Fill(pt)        
        elif quality==5:
            hPtVars[3].Fill(pt)        
        elif quality==7:
            hPtVars[4].Fill(pt)        
        elif quality==0:
            hPtVars[5].Fill(pt)

        if pt>2:
            hPtVars[6].Fill(pt)
        if nStubs>3:
            hPtVars[7].Fill(pt)
        if nStubs>5:
            hPtVars[8].Fill(pt)
            if normalizedChi2<15.:
                hPtVars[9].Fill(pt)


def scaleHistos(hVars):
    for hVar in hVars:
        hVar.Scale(1./hVar.GetSumOfWeights())


#set up labels
topLeft_x_left    = 0.15
y_bottom  = 0.93
topLeft_x_right   = 0.55
y_top     = 0.98

header_x_left    = 0.6
header_x_right   = 0.95

CMSLabel = TPaveLabel(topLeft_x_left,y_bottom,topLeft_x_right,y_top,"CMS #bf{#it{Simulation Preliminary}}","NDC")
CMSLabel.SetTextFont(62)
CMSLabel.SetTextSize(0.8)
CMSLabel.SetTextAlign(12)
CMSLabel.SetBorderSize(0)
CMSLabel.SetFillColor(0)
CMSLabel.SetFillStyle(0)

HeaderLabel = TPaveLabel(header_x_left,y_bottom,header_x_right,y_top,"t#bar{t} PU200","NDC")
HeaderLabel.SetTextAlign(32)
HeaderLabel.SetTextFont(42)
HeaderLabel.SetTextSize(0.697674)
HeaderLabel.SetBorderSize(0)
HeaderLabel.SetFillColor(0)
HeaderLabel.SetFillStyle(0)


#set up canvases
CanvasPt_0 = TCanvas("canvasPt_0","")
CanvasPt_0.SetHighLightColor(2)
CanvasPt_0.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasPt_0.SetFillColor(0)
CanvasPt_0.SetBorderMode(0)
CanvasPt_0.SetBorderSize(2)
CanvasPt_0.SetTickx(1)
CanvasPt_0.SetTicky(1)
CanvasPt_0.SetFrameBorderMode(0)
CanvasPt_0.SetFrameBorderMode(0)
CanvasPt_0.SetLogy()

CanvasPt_1 = TCanvas("canvasPt_1","")
CanvasPt_1.SetHighLightColor(2)
CanvasPt_1.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasPt_1.SetFillColor(0)
CanvasPt_1.SetBorderMode(0)
CanvasPt_1.SetBorderSize(2)
CanvasPt_1.SetTickx(1)
CanvasPt_1.SetTicky(1)
CanvasPt_1.SetFrameBorderMode(0)
CanvasPt_1.SetFrameBorderMode(0)
CanvasPt_1.SetLogy()


CanvasPtEff_0 = TCanvas("canvasPtEff_0","")
CanvasPtEff_0.SetHighLightColor(2)
CanvasPtEff_0.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasPtEff_0.SetFillColor(0)
CanvasPtEff_0.SetBorderMode(0)
CanvasPtEff_0.SetBorderSize(2)
CanvasPtEff_0.SetTickx(1)
CanvasPtEff_0.SetTicky(1)
CanvasPtEff_0.SetFrameBorderMode(0)
CanvasPtEff_0.SetFrameBorderMode(0)

CanvasPtEff_1 = TCanvas("canvasPtEff_1","")
CanvasPtEff_1.SetHighLightColor(2)
CanvasPtEff_1.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasPtEff_1.SetFillColor(0)
CanvasPtEff_1.SetBorderMode(0)
CanvasPtEff_1.SetBorderSize(2)
CanvasPtEff_1.SetTickx(1)
CanvasPtEff_1.SetTicky(1)
CanvasPtEff_1.SetFrameBorderMode(0)
CanvasPtEff_1.SetFrameBorderMode(0)


CanvasPt = TCanvas("canvasPt","")
CanvasPt.SetHighLightColor(2)
CanvasPt.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasPt.SetFillColor(0)
CanvasPt.SetBorderMode(0)
CanvasPt.SetBorderSize(2)
CanvasPt.SetTickx(1)
CanvasPt.SetTicky(1)
CanvasPt.SetFrameBorderMode(0)
CanvasPt.SetFrameBorderMode(0)
CanvasPt.SetLogy()

CanvasQuality = TCanvas("canvasQuality","")
CanvasQuality.SetHighLightColor(2)
CanvasQuality.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasQuality.SetFillColor(0)
CanvasQuality.SetBorderMode(0)
CanvasQuality.SetBorderSize(2)
CanvasQuality.SetTickx(1)
CanvasQuality.SetTicky(1)
CanvasQuality.SetFrameBorderMode(0)
CanvasQuality.SetFrameBorderMode(0)
CanvasQuality.SetLogy()


CanvasNStubs = TCanvas("canvasNStubs","")
CanvasNStubs.SetHighLightColor(2)
CanvasNStubs.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasNStubs.SetFillColor(0)
CanvasNStubs.SetBorderMode(0)
CanvasNStubs.SetBorderSize(2)
CanvasNStubs.SetTickx(1)
CanvasNStubs.SetTicky(1)
CanvasNStubs.SetFrameBorderMode(0)
CanvasNStubs.SetFrameBorderMode(0)
CanvasNStubs.SetLogy()

CanvasNormalizedChi2 = TCanvas("canvasNormalizedChi2","")
CanvasNormalizedChi2.SetHighLightColor(2)
CanvasNormalizedChi2.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasNormalizedChi2.SetFillColor(0)
CanvasNormalizedChi2.SetBorderMode(0)
CanvasNormalizedChi2.SetBorderSize(2)
CanvasNormalizedChi2.SetTickx(1)
CanvasNormalizedChi2.SetTicky(1)
CanvasNormalizedChi2.SetFrameBorderMode(0)
CanvasNormalizedChi2.SetFrameBorderMode(0)
CanvasNormalizedChi2.SetLogy()

CanvasChi2 = TCanvas("canvasChi2","")
CanvasChi2.SetHighLightColor(2)
CanvasChi2.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasChi2.SetFillColor(0)
CanvasChi2.SetBorderMode(0)
CanvasChi2.SetBorderSize(2)
CanvasChi2.SetTickx(1)
CanvasChi2.SetTicky(1)
CanvasChi2.SetFrameBorderMode(0)
CanvasChi2.SetFrameBorderMode(0)
CanvasChi2.SetLogy()


CanvasTrkWrdRInv = TCanvas("canvasTrkWrdRInv","")
CanvasTrkWrdRInv.SetHighLightColor(2)
CanvasTrkWrdRInv.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasTrkWrdRInv.SetFillColor(0)
CanvasTrkWrdRInv.SetBorderMode(0)
CanvasTrkWrdRInv.SetBorderSize(2)
CanvasTrkWrdRInv.SetTickx(1)
CanvasTrkWrdRInv.SetTicky(1)
CanvasTrkWrdRInv.SetFrameBorderMode(0)
CanvasTrkWrdRInv.SetFrameBorderMode(0)
CanvasTrkWrdRInv.SetLogy()

CanvasTrkWrdPhi = TCanvas("canvasTrkWrdPhi","")
CanvasTrkWrdPhi.SetHighLightColor(2)
CanvasTrkWrdPhi.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasTrkWrdPhi.SetFillColor(0)
CanvasTrkWrdPhi.SetBorderMode(0)
CanvasTrkWrdPhi.SetBorderSize(2)
CanvasTrkWrdPhi.SetTickx(1)
CanvasTrkWrdPhi.SetTicky(1)
CanvasTrkWrdPhi.SetFrameBorderMode(0)
CanvasTrkWrdPhi.SetFrameBorderMode(0)
CanvasTrkWrdPhi.SetLogy()


CanvasTrkWrdTanl = TCanvas("canvasTrkWrdTanl","")
CanvasTrkWrdTanl.SetHighLightColor(2)
CanvasTrkWrdTanl.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasTrkWrdTanl.SetFillColor(0)
CanvasTrkWrdTanl.SetBorderMode(0)
CanvasTrkWrdTanl.SetBorderSize(2)
CanvasTrkWrdTanl.SetTickx(1)
CanvasTrkWrdTanl.SetTicky(1)
CanvasTrkWrdTanl.SetFrameBorderMode(0)
CanvasTrkWrdTanl.SetFrameBorderMode(0)
CanvasTrkWrdTanl.SetLogy()

CanvasTrkWrdZ0 = TCanvas("canvasTrkWrdZ0","")
CanvasTrkWrdZ0.SetHighLightColor(2)
CanvasTrkWrdZ0.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasTrkWrdZ0.SetFillColor(0)
CanvasTrkWrdZ0.SetBorderMode(0)
CanvasTrkWrdZ0.SetBorderSize(2)
CanvasTrkWrdZ0.SetTickx(1)
CanvasTrkWrdZ0.SetTicky(1)
CanvasTrkWrdZ0.SetFrameBorderMode(0)
CanvasTrkWrdZ0.SetFrameBorderMode(0)
CanvasTrkWrdZ0.SetLogy()

CanvasTrkWrdD0 = TCanvas("canvasTrkWrdD0","")
CanvasTrkWrdD0.SetHighLightColor(2)
CanvasTrkWrdD0.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasTrkWrdD0.SetFillColor(0)
CanvasTrkWrdD0.SetBorderMode(0)
CanvasTrkWrdD0.SetBorderSize(2)
CanvasTrkWrdD0.SetTickx(1)
CanvasTrkWrdD0.SetTicky(1)
CanvasTrkWrdD0.SetFrameBorderMode(0)
CanvasTrkWrdD0.SetFrameBorderMode(0)
CanvasTrkWrdD0.SetLogy()

CanvasTrkWrdChi2RPhi = TCanvas("canvasTrkWrdChi2RPhi","")
CanvasTrkWrdChi2RPhi.SetHighLightColor(2)
CanvasTrkWrdChi2RPhi.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasTrkWrdChi2RPhi.SetFillColor(0)
CanvasTrkWrdChi2RPhi.SetBorderMode(0)
CanvasTrkWrdChi2RPhi.SetBorderSize(2)
CanvasTrkWrdChi2RPhi.SetTickx(1)
CanvasTrkWrdChi2RPhi.SetTicky(1)
CanvasTrkWrdChi2RPhi.SetFrameBorderMode(0)
CanvasTrkWrdChi2RPhi.SetFrameBorderMode(0)
CanvasTrkWrdChi2RPhi.SetLogy()

CanvasTrkWrdChi2RZ = TCanvas("canvasTrkWrdChi2RZ","")
CanvasTrkWrdChi2RZ.SetHighLightColor(2)
CanvasTrkWrdChi2RZ.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasTrkWrdChi2RZ.SetFillColor(0)
CanvasTrkWrdChi2RZ.SetBorderMode(0)
CanvasTrkWrdChi2RZ.SetBorderSize(2)
CanvasTrkWrdChi2RZ.SetTickx(1)
CanvasTrkWrdChi2RZ.SetTicky(1)
CanvasTrkWrdChi2RZ.SetFrameBorderMode(0)
CanvasTrkWrdChi2RZ.SetFrameBorderMode(0)
CanvasTrkWrdChi2RZ.SetLogy()

CanvasTrkWrdBendChi2 = TCanvas("canvasTrkWrdBendChi2","")
CanvasTrkWrdBendChi2.SetHighLightColor(2)
CanvasTrkWrdBendChi2.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasTrkWrdBendChi2.SetFillColor(0)
CanvasTrkWrdBendChi2.SetBorderMode(0)
CanvasTrkWrdBendChi2.SetBorderSize(2)
CanvasTrkWrdBendChi2.SetTickx(1)
CanvasTrkWrdBendChi2.SetTicky(1)
CanvasTrkWrdBendChi2.SetFrameBorderMode(0)
CanvasTrkWrdBendChi2.SetFrameBorderMode(0)
CanvasTrkWrdBendChi2.SetLogy()

CanvasTrkWrdHitPattern = TCanvas("canvasTrkWrdHitPattern","")
CanvasTrkWrdHitPattern.SetHighLightColor(2)
CanvasTrkWrdHitPattern.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasTrkWrdHitPattern.SetFillColor(0)
CanvasTrkWrdHitPattern.SetBorderMode(0)
CanvasTrkWrdHitPattern.SetBorderSize(2)
CanvasTrkWrdHitPattern.SetTickx(1)
CanvasTrkWrdHitPattern.SetTicky(1)
CanvasTrkWrdHitPattern.SetFrameBorderMode(0)
CanvasTrkWrdHitPattern.SetFrameBorderMode(0)
CanvasTrkWrdHitPattern.SetLogy()

CanvasTrkWrdMVAQuality = TCanvas("canvasTrkWrdMVAQuality","")
CanvasTrkWrdMVAQuality.SetHighLightColor(2)
CanvasTrkWrdMVAQuality.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasTrkWrdMVAQuality.SetFillColor(0)
CanvasTrkWrdMVAQuality.SetBorderMode(0)
CanvasTrkWrdMVAQuality.SetBorderSize(2)
CanvasTrkWrdMVAQuality.SetTickx(1)
CanvasTrkWrdMVAQuality.SetTicky(1)
CanvasTrkWrdMVAQuality.SetFrameBorderMode(0)
CanvasTrkWrdMVAQuality.SetFrameBorderMode(0)
CanvasTrkWrdMVAQuality.SetLogy()

CanvasTrkWrdMVAOther = TCanvas("canvasTrkWrdMVAOther","")
CanvasTrkWrdMVAOther.SetHighLightColor(2)
CanvasTrkWrdMVAOther.Range(-72.16495,-10.50091,516.9367,82.84142)
CanvasTrkWrdMVAOther.SetFillColor(0)
CanvasTrkWrdMVAOther.SetBorderMode(0)
CanvasTrkWrdMVAOther.SetBorderSize(2)
CanvasTrkWrdMVAOther.SetTickx(1)
CanvasTrkWrdMVAOther.SetTicky(1)
CanvasTrkWrdMVAOther.SetFrameBorderMode(0)
CanvasTrkWrdMVAOther.SetFrameBorderMode(0)
CanvasTrkWrdMVAOther.SetLogy()


inputFiles = [TFile("/afs/cern.ch/work/j/jalimena/P2L1Tracks/CMSSW_11_1_7/src/FastPUPPI/NtupleProducer/python/idTuple_TTbar_PU200.110X_v2.root"),
              TFile("/afs/cern.ch/work/j/jalimena/P2L1Tracks/CMSSW_12_3_0_pre4/src/FastPUPPI/NtupleProducer/python/idTuple_TTbar_PU200.110X_v3.root"),
          ]


#set up histograms
hPt_effDummy = TH1F("hPt_effDummy","",100,0,100)
hPt_effDummy.SetTitle(";p_{T} [GeV];Efficiency/ GeV")

hPt = TH1F("hPt","",100,0,100)
hPt.SetTitle(";p_{T} [GeV];Events/ GeV")
hPt.SetLineWidth(2)
hPt.SetLineColor(1)

hPt_PFloose = hPt.Clone()
hPt_PFloose.SetLineColor(2)
hPt_PFloose.SetFillColor(2)

hPt_PFtight = hPt.Clone()
hPt_PFtight.SetLineColor(8)
hPt_PFtight.SetFillColor(8)

hPt_PFtightAndEgamma = hPt.Clone()
hPt_PFtightAndEgamma.SetLineColor(4)
hPt_PFtightAndEgamma.SetFillColor(4)

hPt_PFlooseAndEgamma = hPt.Clone()
hPt_PFlooseAndEgamma.SetLineColor(6)
hPt_PFlooseAndEgamma.SetFillColor(6)

hPt_Egamma = hPt.Clone()
hPt_Egamma.SetLineColor(7)
hPt_Egamma.SetFillColor(7)

hPt_noQuality = hPt.Clone()
hPt_noQuality.SetLineColor(14)
hPt_noQuality.SetFillColor(14)

hPt_ptCut = hPt.Clone()
hPt_ptAnd4nStubsCut = hPt.Clone()
hPt_ptAnd6nStubsCut = hPt.Clone()
hPt_ptAnd6nStubsAndNormChisqCut = hPt.Clone()


hStack = THStack("hstack","")
hStack.SetTitle(";p_{T} [GeV];Events/ GeV")
hStack.Add(hPt_noQuality)
hStack.Add(hPt_Egamma)
hStack.Add(hPt_PFlooseAndEgamma)
hStack.Add(hPt_PFtightAndEgamma)
hStack.Add(hPt_PFtight)
hStack.Add(hPt_PFloose)


#set up legend
x_left = 0.5
x_right = 0.9
y_min = 0.5
y_max = 0.8

Legend = TLegend(x_left,y_min,x_right,y_max)
Legend.SetBorderSize(0)
Legend.SetFillColor(0)
Legend.SetFillStyle(0)

Legend.AddEntry(hPt,"All events","L")
Legend.AddEntry(hPt_PFloose,"Only PF loose","F")
Legend.AddEntry(hPt_PFtight,"PF tight","F")
Legend.AddEntry(hPt_Egamma,"Only egamma","F")
Legend.AddEntry(hPt_PFlooseAndEgamma,"PF loose and egamma","F")
Legend.AddEntry(hPt_PFtightAndEgamma,"PF tight and egamma","F")
Legend.AddEntry(hPt_noQuality,"No quality","F")


hQuality = TH1F("hQuality","",8,-0.5,7.5)
hQuality.SetTitle(";Quality;Events")
hQuality.SetLineWidth(3)
hQuality.SetLineColor(1)

hNStubs = TH1F("hNStubs","",7,-0.5,6.5)
hNStubs.SetTitle(";Number of stubs;Events")
hNStubs.SetLineWidth(3)
hNStubs.SetLineColor(1)

hNormalizedChi2 = TH1F("hNormalizedChi2","",100,0,100)
hNormalizedChi2.SetTitle(";#chi^{2}/dof;Events")
hNormalizedChi2.SetLineWidth(3)
hNormalizedChi2.SetLineColor(1)

hChi2 = TH1F("hChi2","",100,0,100)
hChi2.SetTitle(";#chi^{2};Events")
hChi2.SetLineWidth(3)
hChi2.SetLineColor(1)


hTrkWrdRInv = TH1F("hTrkWrdRInv","",100,-0.006,0.006)
hTrkWrdRInv.SetTitle(";Track Word r-inv;Events")
hTrkWrdRInv.SetLineWidth(3)
hTrkWrdRInv.SetLineColor(1)

hTrkWrdPhi = TH1F("hTrkWrdPhi","",32,-3.2,3.2)
hTrkWrdPhi.SetTitle(";Track Word #phi;Events")
hTrkWrdPhi.SetLineWidth(3)
hTrkWrdPhi.SetLineColor(1)

hTrkWrdTanl = TH1F("hTrkWrdTanl","",100,-6,6)
hTrkWrdTanl.SetTitle(";Track Word tan(l);Events")
hTrkWrdTanl.SetLineWidth(3)
hTrkWrdTanl.SetLineColor(1)

hTrkWrdZ0 = TH1F("hTrkWrdZ0","",30,-15,15)
hTrkWrdZ0.SetTitle(";Track Word z_{0};Events")
hTrkWrdZ0.SetLineWidth(3)
hTrkWrdZ0.SetLineColor(1)

hTrkWrdD0 = TH1F("hTrkWrdD0","",10,-1,1)
hTrkWrdD0.SetTitle(";Track Word d_{0};Events")
hTrkWrdD0.SetLineWidth(3)
hTrkWrdD0.SetLineColor(1)

hTrkWrdChi2RPhi = TH1F("hTrkWrdChi2RPhi","",100,0,20)
hTrkWrdChi2RPhi.SetTitle(";Track Word #chi^{2} r-#phi;Events")
hTrkWrdChi2RPhi.SetLineWidth(3)
hTrkWrdChi2RPhi.SetLineColor(1)

hTrkWrdChi2RZ = TH1F("hTrkWrdChi2RZ","",100,0,20)
hTrkWrdChi2RZ.SetTitle(";Track Word #chi^{2} r-z;Events")
hTrkWrdChi2RZ.SetLineWidth(3)
hTrkWrdChi2RZ.SetLineColor(1)

hTrkWrdBendChi2 = TH1F("hTrkWrdBendChi2","",100,0,20)
hTrkWrdBendChi2.SetTitle(";Track Word Bend #chi^{2};Events")
hTrkWrdBendChi2.SetLineWidth(3)
hTrkWrdBendChi2.SetLineColor(1)

hTrkWrdHitPattern = TH1F("hTrkWrdHitPattern","",130,0,130)
hTrkWrdHitPattern.SetTitle(";Track Word Hit Pattern;Events")
hTrkWrdHitPattern.SetLineWidth(3)
hTrkWrdHitPattern.SetLineColor(1)

hTrkWrdMVAQuality = TH1F("hTrkWrdMVAQuality","",2,-1,1)
hTrkWrdMVAQuality.SetTitle(";Track Word MVA Quality;Events")
hTrkWrdMVAQuality.SetLineWidth(3)
hTrkWrdMVAQuality.SetLineColor(1)

hTrkWrdMVAOther = TH1F("hTrkWrdMVAOther","",8,0,8)
hTrkWrdMVAOther.SetTitle(";Track Word MVA Other;Events")
hTrkWrdMVAOther.SetLineWidth(3)
hTrkWrdMVAOther.SetLineColor(1)




#12_3_X copy of plots

hPt_PFloose_1 = hPt_PFloose.Clone()
hPt_PFtight_1 = hPt_PFtight.Clone()
hPt_PFtightAndEgamma_1 = hPt_PFtightAndEgamma.Clone()
hPt_PFlooseAndEgamma_1 = hPt_PFlooseAndEgamma.Clone()
hPt_Egamma_1 = hPt_Egamma.Clone()
hPt_noQuality_1 = hPt_noQuality.Clone()
hPt_ptCut_1 = hPt_ptCut.Clone()
hPt_ptAnd4nStubsCut_1 = hPt_ptAnd4nStubsCut.Clone()
hPt_ptAnd6nStubsCut_1 = hPt_ptAnd6nStubsCut.Clone()
hPt_ptAnd6nStubsAndNormChisqCut_1 = hPt_ptAnd6nStubsAndNormChisqCut.Clone()

hStack_1 = hStack.Clone()
hStack_1.Add(hPt_noQuality_1)
hStack_1.Add(hPt_Egamma_1)
hStack_1.Add(hPt_PFlooseAndEgamma_1)
hStack_1.Add(hPt_PFtightAndEgamma_1)
hStack_1.Add(hPt_PFtight_1)
hStack_1.Add(hPt_PFloose_1)

hPt_1 = hPt.Clone()
hPt_1.SetLineColor(2)

hQuality_1 = hQuality.Clone()
hQuality_1.SetLineColor(2)

hNStubs_1 = hNStubs.Clone()
hNStubs_1.SetLineColor(2)

hNormalizedChi2_1 = hNormalizedChi2.Clone()
hNormalizedChi2_1.SetLineColor(2)

hChi2_1 = hChi2.Clone()
hChi2_1.SetLineColor(2)

hTrkWrdRInv_1 = hTrkWrdRInv.Clone()
hTrkWrdRInv_1.SetLineColor(2)

hTrkWrdPhi_1 = hTrkWrdPhi.Clone()
hTrkWrdPhi_1.SetLineColor(2)

hTrkWrdTanl_1 = hTrkWrdTanl.Clone()
hTrkWrdTanl_1.SetLineColor(2)

hTrkWrdZ0_1 = hTrkWrdZ0.Clone()
hTrkWrdZ0_1.SetLineColor(2)

hTrkWrdD0_1 = hTrkWrdD0.Clone()
hTrkWrdD0_1.SetLineColor(2)

hTrkWrdChi2RPhi_1 = hTrkWrdChi2RPhi.Clone()
hTrkWrdChi2RPhi_1.SetLineColor(2)

hTrkWrdChi2RZ_1 = hTrkWrdChi2RZ.Clone()
hTrkWrdChi2RZ_1.SetLineColor(2)

hTrkWrdBendChi2_1 = hTrkWrdBendChi2.Clone()
hTrkWrdBendChi2_1.SetLineColor(2)

hTrkWrdHitPattern_1 = hTrkWrdHitPattern.Clone()
hTrkWrdHitPattern_1.SetLineColor(2)

hTrkWrdMVAQuality_1 = hTrkWrdMVAQuality.Clone()
hTrkWrdMVAQuality_1.SetLineColor(2)

hTrkWrdMVAOther_1 = hTrkWrdMVAOther.Clone()
hTrkWrdMVAOther_1.SetLineColor(2)


Legend_11vs12 = TLegend(x_left,0.75,x_right,0.9)
Legend_11vs12.SetBorderSize(0)
Legend_11vs12.SetFillColor(0)
Legend_11vs12.SetFillStyle(0)

Legend_11vs12.AddEntry(hQuality,"11_1_X","L")
Legend_11vs12.AddEntry(hQuality_1,"12_3_X","L")



hVars = [
    hPt,
    hQuality,
    hNStubs,
    hNormalizedChi2,
    hChi2,
    hTrkWrdRInv,
    hTrkWrdPhi,
    hTrkWrdTanl,
    hTrkWrdZ0,
    hTrkWrdD0,
    hTrkWrdChi2RPhi,
    hTrkWrdChi2RZ,
    hTrkWrdBendChi2,
    hTrkWrdHitPattern,
    hTrkWrdMVAQuality,
    hTrkWrdMVAOther,
]

hPtVars = [
    hPt_PFloose,
    hPt_PFtight,
    hPt_Egamma,
    hPt_PFlooseAndEgamma,
    hPt_PFtightAndEgamma,
    hPt_noQuality,
    hPt_ptCut,
    hPt_ptAnd4nStubsCut,
    hPt_ptAnd6nStubsCut,
    hPt_ptAnd6nStubsAndNormChisqCut,
]

variables = ["pt",
             "quality",
             "nStubs",
             "normalizedChi2",
             "chi2",
             "trkWrd_rinv",
             "trkWrd_phi",
             "trkWrd_tanl",
             "trkWrd_z0",
             "trkWrd_d0",
             "trkWrd_chi2RPhi",
             "trkWrd_chi2RZ",
             "trkWrd_bendChi2",
             "trkWrd_hitPattern",
             "trkWrd_mvaQuality",
             "trkWrd_mvaOther",
         ]

for iFile, inputFile in enumerate(inputFiles):
    print("iFile is: "+str(iFile))

    if iFile==1:

        hVars = [
            hPt_1,
            hQuality_1,
            hNStubs_1,
            hNormalizedChi2_1,
            hChi2_1,
            hTrkWrdRInv_1,
            hTrkWrdPhi_1,
            hTrkWrdTanl_1,
            hTrkWrdZ0_1,
            hTrkWrdD0_1,
            hTrkWrdChi2RPhi_1,
            hTrkWrdChi2RZ_1,
            hTrkWrdBendChi2_1,
            hTrkWrdHitPattern_1,
            hTrkWrdMVAQuality_1,
            hTrkWrdMVAOther_1,
        ]

        hPtVars = [
            hPt_PFloose_1,
            hPt_PFtight_1,
            hPt_Egamma_1,
            hPt_PFlooseAndEgamma_1,
            hPt_PFtightAndEgamma_1,
            hPt_noQuality_1,
            hPt_ptCut_1,
            hPt_ptAnd4nStubsCut_1,
            hPt_ptAnd6nStubsCut_1,
            hPt_ptAnd6nStubsAndNormChisqCut_1,
        ]

    fillHistos(inputFile,variables,hVars,hPtVars)

hPt_unscaled = hPt.Clone()
hPt_1_unscaled = hPt_1.Clone()

for iFile, inputFile in enumerate(inputFiles):
    if iFile==0:
        hVars = [
            hPt,
            hQuality,
            hNStubs,
            hNormalizedChi2,
            hChi2,
            hTrkWrdRInv,
            hTrkWrdPhi,
            hTrkWrdTanl,
            hTrkWrdZ0,
            hTrkWrdD0,
            hTrkWrdChi2RPhi,
            hTrkWrdChi2RZ,
            hTrkWrdBendChi2,
            hTrkWrdHitPattern,
            hTrkWrdMVAQuality,
            hTrkWrdMVAOther,
        ]

    elif iFile==1:
        hVars = [
            hPt_1,
            hQuality_1,
            hNStubs_1,
            hNormalizedChi2_1,
            hChi2_1,
            hTrkWrdRInv_1,
            hTrkWrdPhi_1,
            hTrkWrdTanl_1,
            hTrkWrdZ0_1,
            hTrkWrdD0_1,
            hTrkWrdChi2RPhi_1,
            hTrkWrdChi2RZ_1,
            hTrkWrdBendChi2_1,
            hTrkWrdHitPattern_1,
            hTrkWrdMVAQuality_1,
            hTrkWrdMVAOther_1,
        ]
    scaleHistos(hVars)


#make efficiency plots
#PF loose = only PF loose + PF tight + PF loose and egamma + PF tight and egamma
#PF tight = PF tight + PF tight and egamma

hPt_totPFloose = hPt_PFloose.Clone()
hPt_totPFloose.Add(hPt_PFtight)
hPt_totPFloose.Add(hPt_PFlooseAndEgamma)
hPt_totPFloose.Add(hPt_PFtightAndEgamma)
#hPt_totPFloose.Rebin(5)

hPt_totPFtight = hPt_PFtight.Clone()
hPt_totPFtight.Add(hPt_PFtightAndEgamma)
#hPt_totPFtight.Rebin(5)

hPt_rebinned = hPt_unscaled.Clone()
#hPt_rebinned.Rebin(5)

hPt_totPFloose.SetLineColor(1)
hPt_totPFtight.SetLineColor(2)
hPt_totPFloose.SetFillColor(0)
hPt_totPFtight.SetFillColor(0)

hPt_effPFloose = TEfficiency(hPt_totPFloose,hPt_rebinned)
hPt_effPFtight = TEfficiency(hPt_totPFtight,hPt_rebinned)
hPt_effPtCut = TEfficiency(hPt_ptCut,hPt_rebinned)
hPt_effPtAnd4nStubsCut = TEfficiency(hPt_ptAnd4nStubsCut,hPt_rebinned)
hPt_effPtAnd6nStubsCut = TEfficiency(hPt_ptAnd6nStubsCut,hPt_rebinned)
hPt_effPtAnd6nStubsAndNormChisqCut = TEfficiency(hPt_ptAnd6nStubsAndNormChisqCut,hPt_rebinned)

hPt_effPFtight.SetLineColor(2)
hPt_effPFtight.SetMarkerColor(2)
hPt_effPtCut.SetLineColor(4)
hPt_effPtCut.SetMarkerColor(4)
hPt_effPtAnd4nStubsCut.SetLineColor(6)
hPt_effPtAnd4nStubsCut.SetMarkerColor(6)
hPt_effPtAnd6nStubsCut.SetLineColor(7)
hPt_effPtAnd6nStubsCut.SetMarkerColor(7)
hPt_effPtAnd6nStubsAndNormChisqCut.SetLineColor(8)
hPt_effPtAnd6nStubsAndNormChisqCut.SetMarkerColor(8)

hPt_effPFloose.SetMarkerStyle(20)
hPt_effPFtight.SetMarkerStyle(21)
hPt_effPtCut.SetMarkerStyle(22)
hPt_effPtAnd4nStubsCut.SetMarkerStyle(23)
hPt_effPtAnd6nStubsCut.SetMarkerStyle(24)
hPt_effPtAnd6nStubsAndNormChisqCut.SetMarkerStyle(25)

hPt_effPFloose.SetTitle(";p_{T} [GeV];Efficiency/ GeV")





hPt_totPFloose_1 = hPt_PFloose_1.Clone()
hPt_totPFloose_1.Add(hPt_PFtight_1)
hPt_totPFloose_1.Add(hPt_PFlooseAndEgamma_1)
hPt_totPFloose_1.Add(hPt_PFtightAndEgamma_1)
#hPt_totPFloose_1.Rebin(5)

hPt_totPFtight_1 = hPt_PFtight_1.Clone()
hPt_totPFtight_1.Add(hPt_PFtightAndEgamma_1)
#hPt_totPFtight_1.Rebin(5)

hPt_rebinned_1 = hPt_1_unscaled.Clone()
#hPt_rebinned_1.Rebin(5)

hPt_totPFloose_1.SetLineColor(1)
hPt_totPFtight_1.SetLineColor(2)
hPt_totPFloose_1.SetFillColor(0)
hPt_totPFtight_1.SetFillColor(0)

hPt_effPFloose_1 = TEfficiency(hPt_totPFloose_1,hPt_rebinned_1)
hPt_effPFtight_1 = TEfficiency(hPt_totPFtight_1,hPt_rebinned_1)
hPt_effPtCut_1 = TEfficiency(hPt_ptCut_1,hPt_rebinned_1)
hPt_effPtAnd4nStubsCut_1 = TEfficiency(hPt_ptAnd4nStubsCut_1,hPt_rebinned_1)
hPt_effPtAnd6nStubsCut_1 = TEfficiency(hPt_ptAnd6nStubsCut_1,hPt_rebinned_1)
hPt_effPtAnd6nStubsAndNormChisqCut_1 = TEfficiency(hPt_ptAnd6nStubsAndNormChisqCut_1,hPt_rebinned_1)

hPt_effPFtight_1.SetLineColor(2)
hPt_effPFtight_1.SetMarkerColor(2)
hPt_effPtCut_1.SetLineColor(4)
hPt_effPtCut_1.SetMarkerColor(4)
hPt_effPtAnd4nStubsCut_1.SetLineColor(6)
hPt_effPtAnd4nStubsCut_1.SetMarkerColor(6)
hPt_effPtAnd6nStubsCut_1.SetLineColor(7)
hPt_effPtAnd6nStubsCut_1.SetMarkerColor(7)
hPt_effPtAnd6nStubsAndNormChisqCut_1.SetLineColor(8)
hPt_effPtAnd6nStubsAndNormChisqCut_1.SetMarkerColor(8)

hPt_effPFloose_1.SetMarkerStyle(20)
hPt_effPFtight_1.SetMarkerStyle(21)
hPt_effPtCut_1.SetMarkerStyle(22)
hPt_effPtAnd4nStubsCut_1.SetMarkerStyle(23)
hPt_effPtAnd6nStubsCut_1.SetMarkerStyle(24)
hPt_effPtAnd6nStubsAndNormChisqCut_1.SetMarkerStyle(25)

hPt_effPFloose_1.SetTitle(";p_{T} [GeV];Efficiency/ GeV")



LegendEff = TLegend(0.2,0.15,0.7,0.45)
LegendEff.SetBorderSize(0)
LegendEff.SetFillColor(0)
LegendEff.SetFillStyle(0)
LegendEff.AddEntry(hPt_effPtCut,"p_{T} > 2 GeV","P")
LegendEff.AddEntry(hPt_effPtAnd4nStubsCut,"p_{T} > 2 GeV & >= 4 stubs","P")
LegendEff.AddEntry(hPt_effPFloose,"PF loose","P")
LegendEff.AddEntry(hPt_effPtAnd6nStubsCut,"p_{T} > 2 GeV & >= 6 stubs","P")
LegendEff.AddEntry(hPt_effPtAnd6nStubsAndNormChisqCut,"p_{T} > 2 GeV & >= 6 stubs & #chi^{2}/dof < 15","P")
LegendEff.AddEntry(hPt_effPFtight,"PF tight","P")


for iFile, inputFile in enumerate(inputFiles):    
    if(iFile==0):
        CanvasPt_0.cd()
        hStack.Draw()
        hPt_unscaled.Draw("histsame")
    elif(iFile==1):
        CanvasPt_1.cd()
        hStack_1.Draw()
        hPt_1_unscaled.Draw("histsame")
    Legend.Draw()
    CMSLabel.Draw()
    HeaderLabel.Draw()

    if(iFile==0):
        CanvasPtEff_0.cd()
        hPt_effDummy.Draw()
        hPt_effPFloose.Draw("PEsame")
        hPt_effPFtight.Draw("PEsame")
        hPt_effPtCut.Draw("PEsame")
        hPt_effPtAnd4nStubsCut.Draw("PEsame")
        hPt_effPtAnd6nStubsCut.Draw("PEsame")
        hPt_effPtAnd6nStubsAndNormChisqCut.Draw("PEsame")

    elif(iFile==1):
        CanvasPtEff_1.cd()
        hPt_effDummy.Draw()
        hPt_effPFloose_1.Draw("PEsame")
        hPt_effPFtight_1.Draw("PEsame")
        hPt_effPtCut_1.Draw("PEsame")
        hPt_effPtAnd4nStubsCut_1.Draw("PEsame")
        hPt_effPtAnd6nStubsCut_1.Draw("PEsame")
        hPt_effPtAnd6nStubsAndNormChisqCut_1.Draw("PEsame")
    LegendEff.Draw()
    CMSLabel.Draw()
    HeaderLabel.Draw()

    CanvasPt.cd()
    if(iFile==0):
        hPt.Draw("hist")
    elif(iFile>0):
        hPt_1.Draw("histsame")

    CanvasQuality.cd()
    if(iFile==0):
        hQuality.Draw("hist")
    elif(iFile>0):
        hQuality_1.Draw("histsame")

    CanvasNStubs.cd()
    if(iFile==0):
        hNStubs.Draw("hist")
    elif(iFile>0):
        hNStubs_1.Draw("histsame")

    CanvasNormalizedChi2.cd()
    if(iFile==0):
        hNormalizedChi2.Draw("hist")
    if(iFile>0):
        hNormalizedChi2_1.Draw("histsame")

    CanvasChi2.cd()
    if(iFile==0):
        hChi2.Draw("hist")
    elif(iFile>0):
        hChi2_1.Draw("histsame")

    CanvasTrkWrdRInv.cd()
    if(iFile==0):
        hTrkWrdRInv.Draw("hist")
    elif(iFile>0):
        hTrkWrdRInv_1.Draw("histsame")

    CanvasTrkWrdPhi.cd()
    if(iFile==0):
        hTrkWrdPhi.Draw("hist")
    elif(iFile>0):
        hTrkWrdPhi_1.Draw("histsame")

    CanvasTrkWrdTanl.cd()
    if(iFile==0):
        hTrkWrdTanl.Draw("hist")
    elif(iFile>0):
        hTrkWrdTanl_1.Draw("histsame")

    CanvasTrkWrdZ0.cd()
    if(iFile==0):
        hTrkWrdZ0.Draw("hist")
    elif(iFile>0):
        hTrkWrdZ0_1.Draw("histsame")

    CanvasTrkWrdD0.cd()
    if(iFile==0):
        hTrkWrdD0.Draw("hist")
    elif(iFile>0):
        hTrkWrdD0_1.Draw("histsame")

    CanvasTrkWrdChi2RPhi.cd()
    if(iFile==0):
        hTrkWrdChi2RPhi.Draw("hist")
    elif(iFile>0):
        hTrkWrdChi2RPhi_1.Draw("histsame")

    CanvasTrkWrdChi2RZ.cd()
    if(iFile==0):
        hTrkWrdChi2RZ.Draw("hist")
    elif(iFile>0):
        hTrkWrdChi2RZ_1.Draw("histsame")

    CanvasTrkWrdBendChi2.cd()
    if(iFile==0):
        hTrkWrdBendChi2.Draw("hist")
    elif(iFile>0):
        hTrkWrdBendChi2_1.Draw("histsame")

    CanvasTrkWrdHitPattern.cd()
    if(iFile==0):
        hTrkWrdHitPattern.Draw("hist")
    elif(iFile>0):
        hTrkWrdHitPattern_1.Draw("histsame")

    CanvasTrkWrdMVAQuality.cd()
    if(iFile==0):
        hTrkWrdMVAQuality.Draw("hist")
    elif(iFile>0):
        hTrkWrdMVAQuality_1.Draw("histsame")

    CanvasTrkWrdMVAOther.cd()
    if(iFile==0):
        hTrkWrdMVAOther.Draw("hist")
    elif(iFile>0):
        hTrkWrdMVAOther_1.Draw("histsame")



CanvasPt_0.SaveAs("plots/pt_11_1_X.pdf")
CanvasPt_1.SaveAs("plots/pt_12_3_X.pdf")
CanvasPtEff_0.SaveAs("plots/ptEff_11_1_X.pdf")
CanvasPtEff_1.SaveAs("plots/ptEff_12_3_X.pdf")
    
CanvasPt.cd()
Legend_11vs12.Draw()
CMSLabel.Draw()
HeaderLabel.Draw()
CanvasPt.SaveAs("plots/pt.pdf")

CanvasQuality.cd()
Legend_11vs12.Draw()
CMSLabel.Draw()
HeaderLabel.Draw()
CanvasQuality.SaveAs("plots/quality.pdf")

CanvasNStubs.cd()
Legend_11vs12.Draw()
CMSLabel.Draw()
HeaderLabel.Draw()
CanvasNStubs.SaveAs("plots/nStubs.pdf")

CanvasNormalizedChi2.cd()
Legend_11vs12.Draw()
CMSLabel.Draw()
HeaderLabel.Draw()
CanvasNormalizedChi2.SaveAs("plots/normalizedChi2.pdf")

CanvasChi2.cd()
Legend_11vs12.Draw()
CMSLabel.Draw()
HeaderLabel.Draw()
CanvasChi2.SaveAs("plots/chi2.pdf")

CanvasTrkWrdRInv.cd()
Legend_11vs12.Draw()
CMSLabel.Draw()
HeaderLabel.Draw()
CanvasTrkWrdRInv.SaveAs("plots/trkWrdRInv.pdf")

CanvasTrkWrdPhi.cd()
Legend_11vs12.Draw()
CMSLabel.Draw()
HeaderLabel.Draw()
CanvasTrkWrdPhi.SaveAs("plots/trkWrdPhi.pdf")

CanvasTrkWrdTanl.cd()
Legend_11vs12.Draw()
CMSLabel.Draw()
HeaderLabel.Draw()
CanvasTrkWrdTanl.SaveAs("plots/trkWrdTanl.pdf")

CanvasTrkWrdZ0.cd()
Legend_11vs12.Draw()
CMSLabel.Draw()
HeaderLabel.Draw()
CanvasTrkWrdZ0.SaveAs("plots/trkWrdZ0.pdf")

CanvasTrkWrdD0.cd()
Legend_11vs12.Draw()
CMSLabel.Draw()
HeaderLabel.Draw()
CanvasTrkWrdD0.SaveAs("plots/trkWrdD0.pdf")

CanvasTrkWrdChi2RPhi.cd()
Legend_11vs12.Draw()
CMSLabel.Draw()
HeaderLabel.Draw()
CanvasTrkWrdChi2RPhi.SaveAs("plots/trkWrdChi2RPhi.pdf")

CanvasTrkWrdChi2RZ.cd()
Legend_11vs12.Draw()
CMSLabel.Draw()
HeaderLabel.Draw()
CanvasTrkWrdChi2RZ.SaveAs("plots/trkWrdChi2RZ.pdf")

CanvasTrkWrdBendChi2.cd()
Legend_11vs12.Draw()
CMSLabel.Draw()
HeaderLabel.Draw()
CanvasTrkWrdBendChi2.SaveAs("plots/trkWrdBendChi2.pdf")

CanvasTrkWrdHitPattern.cd()
Legend_11vs12.Draw()
CMSLabel.Draw()
HeaderLabel.Draw()
CanvasTrkWrdHitPattern.SaveAs("plots/trkWrdHitPattern.pdf")

CanvasTrkWrdMVAQuality.cd()
Legend_11vs12.Draw()
CMSLabel.Draw()
HeaderLabel.Draw()
CanvasTrkWrdMVAQuality.SaveAs("plots/trkWrdMVAQuality.pdf")

CanvasTrkWrdMVAOther.cd()
Legend_11vs12.Draw()
CMSLabel.Draw()
HeaderLabel.Draw()
CanvasTrkWrdMVAOther.SaveAs("plots/trkWrdMVAOther.pdf")
