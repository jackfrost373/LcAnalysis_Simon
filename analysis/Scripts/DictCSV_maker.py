#This script is for creating the CVS files for the Analysis Notes

# WE COULD ADD PATH LINKS IF THE DICTIONNARIES ARE NOT IN THE SAME FOLDER
from yearFit_DictFile import mainDict as yearDict
from singleFit_DictFile import mainDict as singleDict
from combinedFit_DictFile import mainDict as combinedDict

FILE_OUT_PATH = "./"


fyear = open(FILE_OUT_PATH + "yearly_yields.csv", 'w+')
fcombined = open(FILE_OUT_PATH + "combined_yields.csv", 'w+')
fsingle = open(FILE_OUT_PATH + "single_yields.csv", 'w+')

fyear.write("Data,{0},{1}\n".format("Yield Value","Yield Error"))
fcombined.write("Data,{0},{1}\n".format("Yield Value","Yield Error"))
fsingle.write("Data,{0},{1}\n".format("Yield Value","Yield Error"))

# FOR YEARLY YIELDS
for i in yearDict:
	for j in yearDict[i]:
		for k in yearDict[i][j]:
			fyear.write("{0} {1} {2},{3},{4}\n".format(k[:-11], i, j, yearDict[i][j][k]["yield_val"], yearDict[i][j][k]["yield_err"]))

# FOR COMBINED YIELDS
for i in combinedDict:
	for j in combinedDict[i]:
		for k in combinedDict[i][j]:
			fcombined.write("{0} {1} {2},{3},{4}\n".format(i, j, k[:-5], combinedDict[i][j][k]["yield_val"], combinedDict[i][j][k]["yield_err"]))

# FOR SINGLE YIELDS
for i in singleDict:
	for j in singleDict[i]:
		for k in singleDict[i][j]:
			fsingle.write("{0} {1} {2},{3},{4}\n".format(i, j, k[:-5], singleDict[i][j][k]["yield_val"], singleDict[i][j][k]["yield_err"]))

