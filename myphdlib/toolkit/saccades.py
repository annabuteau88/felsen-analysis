import numpy as np
from toolkit.process import AnalysisObject
import math


def parseSaccadeType(h5file):
    """
    This function determines which saccades are spontaneous and which are driven
    and returns both arrays
    """
    session = AnalysisObject(h5file)
    start = session.load('stimuli/dg/grating/timestamps')
    stop = session.load('stimuli/dg/iti/timestamps')
    saccades = session.load('saccades/predicted/left/timestamps')[:, 0]
    spontaneous = list()
    driven = list()
    for i, stopTime in enumerate(stop):
        try:
            startTime = start[i + 1]
        except:
            continue
        mask = np.logical_and(saccades > stopTime, saccades < startTime)
        masked = saccades[mask]
        if masked.any():
            masked = list(masked)
            for element in masked:
                spontaneous.append(element)

    spontaneous = np.array(spontaneous)
    driven = list()
    for sac in saccades:
        if sac not in spontaneous:
            driven.append(sac)
    driven = np.array(driven)
    return driven, spontaneous

def calculateSaccadeAmplitudes(h5file, saccades):
    """
    Input either driven or spontaneous saccades and calculate their amplitudes
    """
    session = AnalysisObject(h5file)
    pose = session.load('pose/filtered')
    frameTimes = session.load('frames/left/timestamps')
    totalSaccadeTimes = session.load('saccades/predicted/left/timestamps')[:, 0]
    subsetIndices = list()
    for time in saccades:
        subsetIndices.append(np.where(totalSaccadeTimes == time)[0])
    amplitudes = list()
    for sac in subsetIndices:
        startIndex = sac
        endTime = session.load('saccades/predicted/left/timestamps')[sac, 1]
        if endTime.size != 1:
            amplitudes.append(0)
        relativeEnd = abs(frameTimes - endTime)
        endShape = np.where(relativeEnd == np.min(relativeEnd))[0].shape[0]
        if endShape == 2:
            endIndex = np.where(relativeEnd == np.min(relativeEnd))[0][0]
        else:
            endIndex = int(np.where(relativeEnd == np.min(relativeEnd))[0])
        startPoint = pose[startIndex, 0]
        endPoint = pose[endIndex, 0]
        amplitude = abs(endPoint - startPoint)
        amplitudes.append(amplitude)
    return amplitudes

def calculateSaccadeStartPoint(h5file, saccades):
    """
    Input either driven or spontaneous saccades and calculate their start point
    """
    session = AnalysisObject(h5file)
    pose = session.load('pose/filtered')
    frameTimes = session.load('frames/left/timestamps')
    totalSaccadeTimes = session.load('saccades/predicted/left/timestamps')[:, 0]
    subsetIndices = list()
    for time in saccades:
        subsetIndices.append(np.where(totalSaccadeTimes == time)[0])
    startPoints = list()
    for sac in subsetIndices:
        startIndex = sac
        startPoint = pose[startIndex, 0]
        startPoints.append(float(startPoint))
    return startPoints

def calculateSaccadeEndPoint(h5file, saccades):
    """
    Input either driven or spontaneous saccades and calculate their end point
    """
    session = AnalysisObject(h5file)
    pose = session.load('pose/filtered')
    frameTimes = session.load('frames/left/timestamps')
    totalSaccadeTimes = session.load('saccades/predicted/left/timestamps')[:, 0]
    subsetIndices = list()
    for time in saccades:
        subsetIndices.append(np.where(totalSaccadeTimes == time)[0])
    endPoints = list()
    for sac in subsetIndices:
        endTime = session.load('saccades/predicted/left/timestamps')[sac, 1]
        if endTime.size != 1:
            endPoints.append(0)
        relativeEnd = abs(frameTimes - endTime)
        endShape = np.where(relativeEnd == np.min(relativeEnd))[0].shape[0]
        if endShape == 2:
            endIndex = np.where(relativeEnd == np.min(relativeEnd))[0][0]
        else:
            endIndex = int(np.where(relativeEnd == np.min(relativeEnd))[0])
        endPoint = pose[endIndex, 0]
        endPoints.append(float(endPoint))
    return endPoints

