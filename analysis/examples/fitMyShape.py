
import ROOT


# Generate Gaussian data to play with

x     = ROOT.RooRealVar("x","x",0,200)
mu    = ROOT.RooRealVar("mu","mu",100,0,200)
sigma = ROOT.RooRealVar("sigma","sigma",10,0,20)
myGauss = ROOT.RooGaussian("myGauss","myGauss",x, mu, sigma)

data = myGauss.generate(ROOT.RooArgSet(x), 10000)

frame = x.frame()
data.plotOn(frame)
c1 = ROOT.TCanvas()
frame.Draw()
c1.Update()

#raw_input("generated data. Press enter to continue.")

#fit = "ipatia"
#fit = "apolonios"
#fit= "bukin"
fit= "gaussCB"



#######################
# Ipatia2 from source, e.g.
#  https://github.com/GerhardRaven/P2VV/blob/master/P2VV/RooIpatia2.h
#  Documentation at https://arxiv.org/pdf/1312.5000.pdf
#######################


if( fit == "ipatia" ) :

  # to compile into SO with ROOT, run first line once.
  #ROOT.gROOT.ProcessLine(".L src/RooIpatia2.cxx++g")
  ROOT.gROOT.ProcessLine(".L src/RooIpatia2_cxx.so")

  l    = ROOT.RooRealVar("l","l",1,0,30)
  zeta = ROOT.RooRealVar("zeta","zeta",2,0,10)
  fb   = ROOT.RooRealVar("fb","fb",0.001,0,0.05)
  a    = ROOT.RooRealVar("a","a",3,0,10)
  n    = ROOT.RooRealVar("n","n",1,0,10)
  a2   = ROOT.RooRealVar("a2","a2",3,0,10)
  n2   = ROOT.RooRealVar("n2","n2",1,0,10)
  signalpdf = ROOT.RooIpatia2("signalpdf","ipatia2", x,l,zeta,fb,sigma,mu,a,n,a2,n2)

 

####################  
# Apolonios2 from Ostap. Need to have compiled ostap, see getostap.bash
# See https://lhcb.github.io/ostap-tutorials/ for tutorials
# Did you run '. ostap/install/thisostap.sh' ?
###################

elif( fit == "apolonios" ) :

  import ROOT.Ostap as Ostap
  sigma1 = ROOT.RooRealVar("sigma1","sigma1",10,0,20) 
  sigma2 = ROOT.RooRealVar("sigma2","sigma2",10,0,20) 
  beta   = ROOT.RooRealVar("beta","beta",1,0,10) 
  signalpdf = Ostap.Models.Apolonios2("signalpdf","apolonios2",x,mu,sigma1,sigma2,beta)



####################
# Bukin shape from either Ostap or RooFit
####################

elif(fit=="bukin"):

  Bukin_Xp   = ROOT.RooRealVar("Bukin_Xp", "Peak position",100,0,200 )
  Bukin_Sigp = ROOT.RooRealVar("Bukin_Sigp", "Peak width", 10,0,20)
  Bukin_xi   = ROOT.RooRealVar("Bukin_xi", "Peak asymmetry parameter", 0, -1, 1)
  Bukin_rho1 = ROOT.RooRealVar("Bukin_rho1", "Parameter of the left tail", 0, -1, 1)
  Bukin_rho2 = ROOT.RooRealVar("Bukin_rho2", "Parameter of the right tail", 0, -1, 1)

  # Use Bukin shape from Ostap
  #import ROOT.Ostap as Ostap
  #signalpdf = Ostap.Models.Bukin("signalpdf", "Bukin shape", x, Bukin_Xp, Bukin_Sigp, Bukin_xi, Bukin_rho1, Bukin_rho2)

  # Use Bukin shape from RooFit
  signalpdf = ROOT.RooBukinPdf("signalpdf","Bukin shape", x, Bukin_Xp, Bukin_Sigp, Bukin_xi, Bukin_rho1, Bukin_rho2)




####################
# Build Gauss + Crystal ball Shape from RooFit
# CB is the traditional 'lossy' pdf, and consists of a gaussian core with an exponential tail tothe left.
# CB + Gauss thus consists of two gaussian cores, with shared mean, but potentially different widths.
####################

elif(fit=="gaussCB") :
  
  cb_sigma = ROOT.RooRealVar("CB_sigma", "CB_sigma", 10, 5, 30) # width of CB shape.
  cb_a     = ROOT.RooRealVar("CB_a", "CB_a", 5, 0, 30) # exp. constant: higher = more gaussian
  cb_n     = ROOT.RooRealVar("CB_n", "CB_n", 2, 0, 10) # #sigma (left) to change from gauss to exp.
  myCB     = ROOT.RooCBShape("myCB","Crystal Ball", x, mu, cb_sigma, cb_a, cb_n)

  fracCB    = ROOT.RooRealVar("fracCB", "fracCB", 0.5, 0, 1)  # relative amount of Gauss to CB
  signalpdf = ROOT.RooAddPdf("signalpdf","CB + Gauss", ROOT.RooArgList(myGauss, myCB), ROOT.RooArgList(fracCB) )




else :

  # Default: Gaussian
  print("Warning: No fitshape set, using default Gaussian!")
  signalpdf = myGauss




###########
# Fit etc.
###########

sigYield = ROOT.RooRealVar("sigYield","Signal Yield",data.sumEntries(),0,1e8)
sigShape = ROOT.RooExtendPdf("sigShape","Signal Shape", signalpdf, sigYield)


# simple fitting interface
fitres = sigShape.fitTo(data, ROOT.RooFit.Save())

print("")
print("Status: {0}".format(fitres.status()))  # status of last MINUIT call. 0 = converged
print("Cov. Quality: {0}".format(fitres.covQual())) # status of covariance matrix. 3 = OK.


# lower-level fitting interface
#nll = ROOT.RooNLLVar("nll","-log(L)",sigShape,data)
#m = ROOT.RooMinuit(nll)
#m.optimizeConst(1)
#print("Migrad status: {0}".format(m.migrad()))  # minimizer
#print("Hesse  status: {0}".format(m.hesse()))   # gets errors from second derivative matrix inversion
#print("Minos  status: {0}".format(m.minos()))   # gets errors from likelihood



sigShape.plotOn(frame)
frame.Draw()
c1.Update()

print("Chi2/NDF: {0}".format(frame.chiSquare()))
print("Signal Yield: {0} +- {1}".format(sigYield.getVal(),sigYield.getError()))




if(fit=="gaussCB") :
  # plot the signal components individually
  signalpdf.plotOn(frame, ROOT.RooFit.Components("myGauss"), ROOT.RooFit.LineColor(8), ROOT.RooFit.LineStyle(2) )
  signalpdf.plotOn(frame, ROOT.RooFit.Components("myCB"),    ROOT.RooFit.LineColor(9), ROOT.RooFit.LineStyle(2) )
  frame.Draw()
  c1.Update()
