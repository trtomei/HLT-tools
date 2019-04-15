import math,glob

from CrossSections import crossSections13TeV

#gROOT.Reset()

#Recommended samples to use: QCD with Pt 30-1800, DYToMuMu, DYToEE, WToMuNu, WToENu
samples = ["QCD50to80",
           "QCD80to120",
           "QCD120to170",
           "QCD170to300",
           "QCD300to470",
           "QCD470to600",
           "DYToLL-M10to50",
           "DYToLL-M50",
           "WJetsToLNu"]


ilumi = 18.0e33


def Rate(count,xsec,nevts):
    rate = xsec*ilumi*(count/nevts)
    return rate


def RateErr(count,xsec,nevts):
    rateerr = ((xsec * ilumi)/nevts) * math.sqrt(count)
    return rateerr

rates = []
err = []

for sample in samples:

    xsec = crossSections13TeV[sample][0]*1e-36
    nevts = crossSections13TeV[sample][1]
    count = crossSections13TeV[sample][2]

    print "sample, nevt, count, xsec: ", sample, " ", nevts, " ", count, " ", xsec/1e-36

    rate = Rate(count,xsec,nevts)
    rateerr = RateErr(count,xsec,nevts)
    rateerrsq = pow(rateerr,2)

    rates.append(rate)
    err.append(rateerrsq)


Totrate = sum(rates)

Toterr = math.sqrt(sum(err))

print "The total rate is ", Totrate, " +- ", Toterr
    
