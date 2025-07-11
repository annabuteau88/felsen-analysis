import matplotlib.pyplot as plt
from toolkit.process import AnalysisObject
import numpy as np
import random

def plotPCA3D(pcs, trial_types, dimensions, stimIndex):
    """
    Takes PCA output & plots it in 3D
    """
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot(pcs[dimensions[0],:, 0], pcs[dimensions[1],:, 0], pcs[dimensions[2],:, 0], color='deepskyblue', label=trial_types[0])
    ax.plot(pcs[dimensions[0],:, 1], pcs[dimensions[1],:, 1], pcs[dimensions[2],:, 1], color='magenta', label=trial_types[1])
    ax.plot(pcs[dimensions[0],stimIndex, 1], pcs[dimensions[1],stimIndex, 1], pcs[dimensions[2],stimIndex, 1], color='magenta', marker='o')
    ax.plot(pcs[dimensions[0],stimIndex, 0], pcs[dimensions[1],stimIndex, 0], pcs[dimensions[2],stimIndex, 0], color='deepskyblue', marker='o')
    ax.plot(pcs[dimensions[0],0, 0], pcs[dimensions[1],0, 0], pcs[dimensions[2],0, 0], color='k', marker='o')
    ax.plot(pcs[dimensions[0],0, 1], pcs[dimensions[1],0, 1], pcs[dimensions[2],0, 1], color='k', marker='o')

    ax.set_xlabel('PC' + str(dimensions[0]))
    ax.set_ylabel('PC' + str(dimensions[1]))
    ax.set_zlabel('PC' + str(dimensions[2]))
    ax.legend()
    return ax

def plotPETH(h5file, unitList, events, color, start, stop, step, label, avgOnly=True, fig=None, ax=None):
    """
    Takes ephys & event inputs and plots a basic PETH of each unit with an average
    """
    if fig is None:
        fig, ax = plt.subplots()
    frList = list()
    session = AnalysisObject(h5file)
    population = session._population()
    for unit in population:
        if unit.cluster in unitList:
            t, fr = unit.peth(events, (start, stop), step)
            baseline = np.mean(fr[0:10])
            corrected = fr - baseline
            if avgOnly == False:
                ax.plot(t, corrected, color=color, alpha=0.25)
            frList.append(corrected)
    frAvg = np.mean(frList, axis=0)
    if avgOnly ==True:
        ax.plot(t, frAvg, color=color, label=label)
    else:
        ax.plot(t, frAvg, color='k')

    return fig, ax

def plotKDE(h5file, unitList, events, color, start, stop, step, label, avgOnly=True, fig=None, ax=None):
    """
    Takes ephys & event inputs and plots a basic PETH of each unit with an average
    """
    if fig is None:
        fig, ax = plt.subplots()
    frList = list()
    session = AnalysisObject(h5file)
    population = session._population()
    for unit in population:
        if unit.cluster in unitList:
            t, fr = unit.kde(events, (start, stop), step)
            baseline = np.mean(fr[0:10])
            corrected = fr - baseline
            if avgOnly == False:
                ax.plot(t, corrected, color=color, alpha=0.25)
            frList.append(corrected)
    frAvg = np.mean(frList, axis=0)
    if avgOnly ==True:
        ax.plot(t, frAvg, color=color, label=label)
    else:
        ax.plot(t, frAvg, color='k')

    return fig, ax

def plotUnitDepth(depthDict):
    fig, ax = plt.subplots(figsize=(4,10))
    plt.scatter([random.random() for d in range(len(depthDict['premotor']))], depthDict['premotor'], color='magenta', label='Premotor')
    plt.scatter([random.random() for d in range(len(depthDict['visual']))], depthDict['visual'], color='limegreen', label='Visual')
    plt.scatter([random.random() for d in range(len(depthDict['visuomotor']))], depthDict['visuomotor'], color='blueviolet', label='Visuomotor')
    plt.xlim(-0.5, 1.5)
    plt.ylim(0, 350)
    plt.xticks([])
    ax.invert_yaxis()
    plt.yticks([0, 100, 200, 300], [0, 1, 2, 3])
    ax.tick_params(axis='y', labelsize=12)
    plt.ylabel('Unit Depth (mm)', fontsize=20)
    return fig, ax