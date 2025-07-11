import matplotlib.pyplot as plt
from toolkit.process import AnalysisObject
import numpy as np

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

def plotPETH(h5file, unitList, events, color, start, stop, step, avgOnly=True, fig=None, ax=None):
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
        ax.plot(t, frAvg, color=color)
    else:
        ax.plot(t, frAvg, color='k')

    return fig, ax