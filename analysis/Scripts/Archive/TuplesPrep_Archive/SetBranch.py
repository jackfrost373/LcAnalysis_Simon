import ROOT, os
from ROOT import TChain, TFile

#### This function takes a ROOT file as an input, keeps the variables in useful_vars in the tree and throws the other ones away. The pruned tree is then returned. ###

def setBranch_funct (root_file, extra_variables):

    useful_vars = ["lcplus_MM", "lcplus_P", "lcplus_PT", "lcplus_ETA", "lcplus_RAPIDITY", "lcplus_TIP", "lcplus_IPCHI2_OWNPV", "lcplus_OWNPV_CHI2", "lcplus_TAU", "lcplus_L0HadronDecision_TOS", "pplus_P", "pplus_PT", "pplus_RAPIDITY", "pplus_ETA", "pplus_ProbNNp", "piplus_P", "piplus_PT", "piplus_RAPIDITY", "piplus_ETA", "piplus_ProbNNpi", "pplus_PIDp", "kminus_P", "kminus_PT", "kminus_RAPIDITY", "kminus_ETA", "kminus_ProbNNk", "kminus_PIDK", "PVNTRACKS"] # list of variables kept in the tree
    
    for extra_variable in extra_variables:
        if not (extra_variable == ""): #if extra_variable is something needed, then it will be added to the array
            useful_vars.append(extra_variable)
    
    tfile = root_file  #These 2 lines depend on the type of file fed into the function
    tfile.SetBranchStatus("*", False) #first deactivate all branches
    
    for element in useful_vars: # then reactivate the ones present in useful_vars
        tfile.SetBranchStatus(element, True)

    return tfile # return the pruned TTree


