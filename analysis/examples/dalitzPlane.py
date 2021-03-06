
#################
# Example of Dalitz plot / sPlot
#################


import ROOT

# Get the data
fileloc = "/data/bfys/jdevries/gangadir/workspace/jdevries/LocalXML/31/1/output/Lc2pKpiTuple.root"
cuts = "(1==1)"

f = ROOT.TFile.Open(fileloc, "READONLY")
tree = f.Get("tuple_Lc2pKpi/DecayTree")

addsWeights = True

###############################


if(addsWeights) :
  # If we made an sWeight friend tree: add it, and use sWeights. Make sure same cuts (--> #entries) as swTree!
  swcuts = "lcplus_MM >= 2240 && lcplus_MM <= 2340 && lcplus_P >= 5000 && lcplus_P <= 200000 && lcplus_TAU >= 0 && lcplus_TAU <= 0.007"
  cuttree = tree.CopyTree(swcuts)
  print("cutTree nEvents = {0}".format(cuttree.GetEntries()))
  cuttree.AddFriend("swTree","output/sWeight_swTree.root")
  weightvar = "swTree.sw_sig"
else :
  cuttree = tree
  weightvar = "1"



def invariantMass(p1, p2) :
  # build invariant mass string
  m1  = p1+"_M" ; ptot1 = p1+"_P" ; px1 = p1+"_PX" ; py1 = p1+"_PY" ; pz1 = p1+"_PZ"
  m2  = p2+"_M" ; ptot2 = p2+"_P" ; px2 = p2+"_PX" ; py2 = p2+"_PY" ; pz2 = p2+"_PZ"
  E1 = "sqrt({0}**2 + {1}**2)".format(m1,ptot1)
  E2 = "sqrt({0}**2 + {1}**2)".format(m2,ptot2)
  pvecdot = "({0}*{1} + {2}*{3} + {4}*{5})".format(px1,px2, py1,py2, pz1,pz2)
  M2 = "({0}**2 + {1}**2 + 2*{2}*{3} - 2*{4})".format(m1,m2,E1,E2,pvecdot)
  return M2
  


m2_pK  = invariantMass("pplus","kminus")
m2_Kpi = invariantMass("kminus","piplus")

c1 = ROOT.TCanvas("c1","c1")
ROOT.gStyle.SetOptStat(0)

cuttree.Draw("{0}:{1}>>dalitzHist(100,300e3,2500e3,100,1800e3,5800e3)".format(m2_pK,m2_Kpi), "{0}*{1}".format(cuts,weightvar))
dalitzHist = ROOT.gDirectory.Get("dalitzHist")
dalitzHist.SetTitle("Dalitz plot of pK#pi")
dalitzHist.GetYaxis().SetTitle("m^{2}_{pK} [MeV^{2}/c^{4}]")
dalitzHist.GetXaxis().SetTitle("m^{2}_{K#pi} [MeV^{2}/c^{4}]")

if(addsWeights) :
  # set negative sWeight bin contents to zero for color visibility
  dalitzHist.SetMinimum(0)
  dalitzHist.SetTitle("sWeighed Dalitz plot of pK#pi")

dalitzHist.Draw("colz")
c1.Update()
c1.SaveAs("output/Dalitz.pdf")


