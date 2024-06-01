import numpy as np
import ctypes
import os
from sklearn.neighbors import kneighbors_graph
from sklearn.metrics.pairwise import euclidean_distances
import matplotlib.pyplot as plt
from scipy.stats import chi2
from scipy.stats import f

# define the location of the MST.so file
MST_FILE = os.path.join(os.path.dirname(__file__), "MST.so")

# similarity measure: L2 distance
# X is the data in matrix form
def L2dist(X):
    N = X.shape[0]
    G = np.matmul(X, np.transpose(X))
    g = np.diagonal(G)
    L2 = np.reshape(np.tile(g, N), (N, -1), order="F")+\
         np.reshape(np.tile(g, N), (N, -1), order="C")-\
         2*G
    L2 = np.sqrt(L2)
    return L2

# function for kmst
#    DM:   array of inter-node edge lengths
#     N:   nodes are numbered 0, 1, 2, ..., N-1
#   MST:   array in which edge list of of MST is placed
#  IMST:   number of edges in array MST
#   CST:   sum of edge lengths of edges of tree
#   NIT:   array of nodes not yet in tree
#  NITP:   number of nodes in array NIT
# JI(i):   node of partial MST  closest to node NIT[i]
# UI(i):   length of edge from NIT(i) to JI(i)
#    KP:   next node to be added to array MST
def MSTgraph(distance_matrix, nlig, ngmax):
    voisi = np.zeros(nlig*nlig, dtype = np.int8)
    borne = 1e20
    lig = int(nlig)
    N = int(nlig)
    numgmax = int(ngmax)
    DM = np.zeros((N, N))
    voisiloc = np.zeros((N, N), dtype = np.int64)
    MST = np.zeros((2, N), dtype = np.int64)
    UI = np.zeros(N)
    JI = np.zeros(N, dtype = np.int64)
    NIT = np.zeros(N, dtype = np.int64)
    
    k = 0
    for i in np.arange(lig):
        for j in np.arange(lig):
            DM[i][j] = distance_matrix[k]
            k = k+1
    for i in np.arange(N):
        DM[i][i] = borne

    for numg in np.arange(1, numgmax+1):
        CST = 0
        NITP = int(N-2)
        KP = int(N-1)
        IMST = int(0)
        for i in np.arange(NITP+1):
            NIT[i] = int(i)
            UI[i] = DM[i][KP]
            JI[i] = int(KP)
        while NITP >= 0:
            for i in np.arange(NITP+1):
                NI = int(NIT[i])
                D = DM[NI][KP]
                if UI[i] > D:
                    UI[i] = D
                    JI[i] = int(KP)
            UK = UI[0]
            for i in np.arange(NITP+1):
                if UI[i] <= UK:
                    UK = UI[i]
                    k = i
            MST[0][IMST] = int(NIT[k])
            MST[1][IMST] = int(JI[k])
            
            IMST = int(IMST+1)
            CST = CST+UK
            KP = int(NIT[k])
            
            UI[k] = UI[NITP]
            NIT[k] = int(NIT[NITP])
            JI[k] = int(JI[NITP])
            NITP = int(NITP-1)
        for i in np.arange(IMST):
            voisiloc[MST[0][i]][MST[1][i]] = numg
            voisiloc[MST[1][i]][MST[0][i]] = numg
            DM[MST[0][i]][MST[1][i]] = borne
            DM[MST[1][i]][MST[0][i]] = borne
    for i in np.arange(lig):
        for j in np.arange(lig):
            a0 = voisiloc[i][j]
            if (a0 > 0) and (a0 <= numgmax):
                voisiloc[i][j] = 1
            else:
                voisiloc[i][j] = 0
    k = 0
    for i in np.arange(lig):
        for j in np.arange(lig):
            voisi[k] = voisiloc[i][j]
            k = k+1
    return np.reshape(voisi, (nlig, nlig), order = "F")
    return voisiloc

# plotMST function
# G is the MST (an N by N symmetric matrix of 0s and 1s representing the connections between each node)
# data is the data matrix
# nID are the nodes belonging to sample 1
# mID are the nodes belonging to sample 2
def plotMST(G, data, nID, mID):
    edges = np.nonzero(np.triu(G))
    for i in np.arange(edges[0].size):
        if edges[0][i] in nID and edges[1][i] in nID:
            plt.plot([data[edges[0][i], 0], data[edges[1][i], 0]], [data[edges[0][i], 1], data[edges[1][i], 1]], c="red", alpha=1, zorder=1)
        elif edges[0][i] in mID and edges[1][i] in mID:
            plt.plot([data[edges[0][i], 0], data[edges[1][i], 0]], [data[edges[0][i], 1], data[edges[1][i], 1]], c="blue", alpha=1, zorder=1)
        else:
            plt.plot([data[edges[0][i], 0], data[edges[1][i], 0]], [data[edges[0][i], 1], data[edges[1][i], 1]], c="lime", alpha=1, zorder=1)
    plt.scatter(x=data[nID, 0], y=data[nID, 1], marker="o", c="red", sizes=[8], alpha=1)
    plt.scatter(x=data[mID, 0], y=data[mID, 1], marker="o", c="blue", sizes=[8], alpha=1)
    plt.show()

# as.dist() python counterpart
# we don't really need this function
def as_dist(X):
    return np.tril(X, k=-1)

# mstree function
# note: distance matrix should be in the form returned by L2dist()
# if data matrix is provided, only the euclidean distance is used
# k is the k in K-MST
def kmst(data_matrix=None, distance_matrix=None, k=5):
    if (data_matrix is not None) and (distance_matrix is None):
        distance_matrix = euclidean_distances(data_matrix)
    elif (data_matrix is None) and (distance_matrix is None):
        return None
    nlig = distance_matrix.shape[0]
    distance_matrix = distance_matrix.flatten("F")
    k = 1 if k < 1 else int(k)
    k = 1 if k >= nlig else int(k)
    kmst = MSTgraph(distance_matrix = distance_matrix, nlig = nlig, ngmax = k)
    return kmst

# precompiled c function for mstree
# requires the MST.so shared library file
# to create this, run the following line
# g++ -fPIC -shared -o MST.so MST.cpp
def Ckmst(data_matrix=None, distance_matrix=None, k=5):
    if (data_matrix is not None) and (distance_matrix is None):
        distance_matrix = euclidean_distances(data_matrix)
    elif (data_matrix is None) and (distance_matrix is None):
        return None
    
    clibrary = ctypes.CDLL(MST_FILE)
    mstree = clibrary.MSTgraph
    mstree.restype = ctypes.POINTER(ctypes.c_double)
    
    nlig = distance_matrix.shape[0]
    distance_matrix = distance_matrix.flatten("F").ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    voisi = np.zeros(nlig*nlig, dtype=float).ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    k = 1 if k < 1 else int(k)
    k = 1 if k >= nlig else int(k)
    
    dbl_ptr = mstree(distance_matrix, ctypes.byref(ctypes.c_int(nlig)), ctypes.byref(ctypes.c_int(k)), voisi)
    kmst = np.ctypeslib.as_array(dbl_ptr, (nlig, nlig)).astype("int64")
    return kmst

# k nearest neighbors function
# note: distance matrix should be symmetric
# if data matrix is provided, only the euclidean distance is used
# k is the k in K-NNG
def knng(data_matrix=None, distance_matrix=None, k=5):
    if (data_matrix is not None) and (distance_matrix is None):
        distance_matrix = L2dist(data_matrix)
    elif (data_matrix is None) and (distance_matrix is None):
        return None
    nlig = distance_matrix.shape[0]
    k = 1 if k < 1 else int(k)
    k = 1 if k >= nlig else int(k)
    knng = kneighbors_graph(X = distance_matrix, n_neighbors = k, metric="precomputed").toarray("C").astype("int64")
    return knng

# |G| function
def edge_count(G):
    return 1/2*np.sum(G > 0)

# return the degrees of all nodes in a graph
# G is the graph (not just an upper or lower triangular matrix)
def degrees(G):
    G = G > 0
    di = np.sum(G, 1)
    return di

# C
# this is the number of edge pairs that share a common node
def C(G):
    # N = G.shape[0] # number of nodes
    # Gi2 = np.zeros(N)
    # for i in range(0, N):
    #     Gi2[i] = (2*edge_count(G[i]))**2
    # return 1/2*np.sum(Gi2)-edge_count(G)
    di = degrees(G)
    return 1/2*np.sum(di*(di-1))

# data is the Nxd data matrix
# nID is an array of the nodes (observations) in sample 1
# mID is an array of the nodes (observations) in sample 2
# the hotelling test performs 
def HotellingTest(data, nID, mID, equal_cov=False):
    N = data.shape[0]
    d = data.shape[1]
    X = data[nID, :]
    Y = data[mID, :]
    n = X.shape[0]
    m = Y.shape[0]
    
    Xbar = np.mean(X, 0).reshape((d, 1))
    Ybar = np.mean(Y, 0).reshape((d, 1))
    
    SX = np.cov(X, rowvar=False)
    SY = np.cov(Y, rowvar=False)
    
    if equal_cov == True:
        teststat = ((n*m)/(n+m))*(((Xbar-Ybar).T)@(np.linalg.inv(((n-1)*SX+(m-1)*SY)/(n+m-2)))@(Xbar-Ybar))[0, 0]
        teststat = ((n+m-d-1)/((n+m-2)*d))*teststat
        pval = f.sf(teststat, d, n+m-d-1)
    else:
        teststat = (((Xbar-Ybar).T)@(np.linalg.inv((SX/n)+(SY/m)))@(Xbar-Ybar))[0, 0]
        pval = chi2.sf(teststat, d)
    
    results = {"hotelling.test.statistic" : teststat, "hotelling.pval" : pval}
    return(results)
