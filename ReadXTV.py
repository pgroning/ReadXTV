# -*- coding: utf-8 -*-
import sys
import codecs
from pylab import *
import numpy as np
import matplotlib as mpl
sys.path.append("/home/user/jsmu/scripts/python_help_modules")
import helpFunctions as hf
import xdrlib 


####################################################################################################################
##################### Functions to read xtv file ###################################################################
##################### Work in progress, to read a file it has to be specified down in the ##########################
##################### rawdata = open('../output/Base_Job.xtv').read() string (line 115 right now). #################
####################################################################################################################

def isDone(unpacker):
    # Function to check if the end of the file has been reached
    try:
        unpacker.done()
        return True
    except xdrlib.Error:
        return False

def readHeader():
    ## Function to read the header in a data file. Prints are for debug purposes
    hdrString = data.unpack_bytes()
    xtvMajorV = data.unpack_int()
    xtvMinorV = data.unpack_int()
    revNumber = data.unpack_int()
    xtvRes = data.unpack_int() # single or double precision, should be single
    nUnits = data.unpack_int() #Number of unit blocks (0?)
    nComp = data.unpack_int() # Number of components after header and before data
    nSVar = data.unpack_int() #
    nDVar = data.unpack_int()
    nSChannels = data.unpack_int()
    nDChannels = data.unpack_int()
    dataStart = data.unpack_int()
    dataLen = data.unpack_int()
    nPoints = data.unpack_int()
    spare1 = data.unpack_int()
    spare2 = data.unpack_int()
    spare3 = data.unpack_int()
    spare4 = data.unpack_int()
    fmtString = data.unpack_string()
    unitsSys = data.unpack_string()
    sysName = data.unpack_string()
    osString = data.unpack_string()
    sDate = data.unpack_string()
    sTime = data.unpack_string()
    title = data.unpack_string()
    endOfHeader = data.get_position()
    
    if(debug):
        print "Header variables"
        print hdrString,xtvMajorV,xtvMinorV,revNumber,xtvRes,nUnits,nComp,nSVar,nDVar,nSChannels,dataStart,dataLen,nPoints,spare1, spare2,spare3,spare4,fmtString, unitsSys,sysName,osString,sDate,sTime,title,endOfHeader
        print " "
    
    return hdrString,xtvMajorV,xtvMinorV,revNumber,xtvRes,nUnits,nComp,nSVar,nDVar,nSChannels,dataStart,dataLen,nPoints,spare1, spare2,spare3,spare4,fmtString, unitsSys,sysName,osString,sDate,sTime,title,endOfHeader


def readComponentParameterBlock(startingPosition):
    #Reads a Component Parameter Block (subroutine openblock() in Cxtvdxr.c and xtvxgchdrio() in xtvxrd.c in TRACE source shows how it is
    # printed to binary dxr formate. Prints are for debug purposes
    data.set_position(startingPosition)
    blockType = data.unpack_bytes()
    revision = data.unpack_int()
    blockSize = data.unpack_int()
    compId = data.unpack_int()
    compSId = data.unpack_int()
    comptype = data.unpack_string()
    compTitle = data.unpack_string()
    cDim = data.unpack_int()    
    nTempl = data.unpack_int()    
    nJun = data.unpack_int()    
    nLegs = data.unpack_int()    
    nSVar = data.unpack_int()
    nDVar = data.unpack_int()
    nVect = data.unpack_int()
    nChild = data.unpack_int()
    nDynAx = data.unpack_int()
    lenAuxStrT = data.unpack_string()
    
    if(debug):
        print "Component Parameter Block Variables"
        print "blockType "+blockType    
        print "revision "+str(revision)
        print "blockSize "+str(blockSize)
        print "compId "+str(compId)
        print "compSId "+str(compSId)
        print "comptype "+str(comptype)
        print "compTitle "+str(compTitle)
        print "cDim "+str(cDim)
        print "nTempl "+str(nTempl)
        print "nJun "+str(nJun)
        print "nLegs "+str(nLegs)
        print "nSVar "+str(nSVar)
        print "nDVar "+str(nDVar)
        print "nVect "+str(nVect)
        print "nChild "+str(nChild)
        print "nDynAx "+str(nDynAx)
        print "lenAuxStrT "+lenAuxStrT
        print blockType,revision,blockSize,compId,compId,compSId,hf.removeWhiteSpace(comptype),hf.removeWhiteSpace(compTitle),cDim,nTempl,nJun,nLegs,nSVar,nDVar,nChild,nDynAx,lenAuxStrT
        print " "
        
        return blockType,revision,blockSize,compId,compId,compSId,hf.removeWhiteSpace(comptype),hf.removeWhiteSpace(compTitle),cDim,nTempl,nJun,nLegs,nSVar,nDVar,nChild,nDynAx,lenAuxStrT

##################################################################################################
##################### Test of methods to red xtv file ############################################
##################################################################################################
debug = True


# read the xdr file (trace xtv)
rawdata = open('../output/Base_Job.xtv').read()
data = xdrlib.Unpacker(rawdata)
        

# Get header data variables from the readHeader function
hdrString,xtvMajorV,xtvMinorV,revNumber,xtvRes,nUnits,nComp,nSVar,nDVar,nSChannels,dataStart,dataLen,nPoints,spare1, spare2,spare3,spare4,fmtString, unitsSys,sysName,osString,sDate,sTime,title,endOfHeader = readHeader()

## Read all time steps
#for i in np.arange(1,nPoints+1):
#    ## Prints all time steps
#    startPoint = dataStart+(i-1)*dataLen
#    data.set_position(startPoint)    
#    datalab = data.unpack_bytes()
#    revStamp = data.unpack_bytes()
#    blockDataLen = data.unpack_int()
#    blockDChannels = data.unpack_int()
#    timeStep = data.unpack_float()
#    print timeStep

## Return to end of header start block
data.set_position(endOfHeader)

readComponentParameterBlock(data.get_position())

