# Cross sections for 13 TeV, Fall13 MC. If you're not using Fall13,
# check McM for the correct cross sections.

# NOTE: DO NOT USE QCD SAMPLES TOGETHER WITH THE LEPTON ENRICHED
# SAMPLES IF YOU DON'T KNOW HOW TO TAKE CARE OF DOUBLE COUNTING!!

#[0] is the cross section
#[1] is the total number of events
#[2] is the number of events that pass your trigger

crossSections13TeV={
    ## QCD Cross sections
    'QCD30to50'    :(106900000.,500000.0,  79),  # Tune CP5, 2019
    'QCD50to80'    :(15710000., 350000.0, 251),  # Same
    'QCD80to120'   :(2336000. , 100000.0, 243),  # Same
    'QCD120to170'  :(407300.,    50000.0, 484),  # Same
    'QCD170to300'  :(103500.,    50000.0, 2365), # Same
    'QCD300to470'  :(7475.,       2500.0, 2500),
    'QCD470to600'  :(587.1,       2500.0, 2500),
    'QCD600to800'  :(167.,        2500.0, 2500),
    'QCD800to1000' :(28.25,       2500.0, 2500),
    'QCD1000to1400':(8.195,       2500.0, 2500),
    'QCD1400to1800':(0.7346,      2500.0, 2500),
    'QCD1800'      :(0.1091,      2500.0, 2500),
    #EM Enriched cross sections    
    #the 2nd number for [0] is the EM filtering efficiency you can get from McM website
    'EMEnr20to30'    :(677300000.*0.007),
    'EMEnr30to80'    :(185900000.*0.056),
    'EMEnr80to170'   :(3529000.*0.158),
    #Mu Enriched cross sections
    #the 2nd number for [0] is the MuEnriched filtering efficiency you can get from McM website
    'MuEnr20to30'    :(675300000.*0.0065, 5000., 72.),
    'MuEnr30to50'    :(164400000.*0.0122, 6000., 36.),
    'MuEnr50to80'    :(21930000.*0.0218, 7000., 21.),
    'MuEnr80to120'   :(3000000.*0.0395, 4000., 53.),
    'MuEnr120to170'  :(493200.*0.0473, 5300., 15.),
    'MuEnr170to300'  :(12030.*0.0676, 2500., 100.),
    'MuEnr300to470'  :(7475.*0.0864,2500,185.0),
    'MuEnr470to600'  :(587.1*0.1024,1224,131.0),
    'MuEnr600to800'  :(167.*0.0996),
    'MuEnr800to1000' :(28.25*0.1033),
    'MuEnr1000'      :(8.975*0.1097),
     #W and Z cross sections
    'DYToLL-M10to50' :(16270.0, 100000.0, 1164),  # Tune CUETP8M1, 2018 (where is the newer one???)
    'DYToLL-M50'     :(5343.0,  100000.0, 11883), # Tune CP5, 2019
    'WJetsToLNu'     :(52940.0, 100000.0, 23465)  # Tune CP5, 2019
}
