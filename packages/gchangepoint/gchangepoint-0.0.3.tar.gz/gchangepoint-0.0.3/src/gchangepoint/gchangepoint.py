import numpy as np
import scipy.integrate as integrate
from scipy.stats import norm
from scipy.stats import chi2

import warnings
warnings.filterwarnings("ignore", message="divide by zero encountered") 
warnings.filterwarnings("ignore", message="invalid value encountered")
warnings.filterwarnings("ignore", message="overflow encountered in")
warnings.filterwarnings("ignore", message="The maximum number of subdivisions")
warnings.filterwarnings("ignore", message="The occurrence of roundoff error is detected")

# RHO1
#                   N:   the total number of nodes
#                   s:
#             n_edges:   the size of the graph, the total number of edges
# sum_degrees_squared:   the sum of the squared degree of each node
def rho1(N, s, n_edges, sum_degrees_squared):
    f1 = 4*(N-1)*(2*s*(N-s)-N)
    f2 = ((N+1)*(N-2*s)**2-2*N*(N-1))
    f3 = 4*((N-2*s)**2-N)
    f4 = 4*N*(s-1)*(N-1)*(N-s-1)
    f5 = N*(N-1)*((N-2*s)**2-(N-2))
    f6 = 4*((N-2)*(N-2*s)**2-2*s*(N-s)+N)
    return N*(N-1)*(f1*n_edges+f2*sum_degrees_squared-f3*n_edges**2)/\
           (2*s*(N-s)*(f4*n_edges+f5*sum_degrees_squared-f6*n_edges**2))

# RHO1_RW
#               N:   the total number of nodes (observations/time points)
#               t:   the time point (index from 1 to N)
def rho1_Rw(N, t):
    return np.float64(-((2*t**2-2*N*t+N)*(N**2-3*N+2)**4))/(2*t*(N-1)**3*(N-2)**4*(t-1)*(N**2-2*N*t-N+t**2+t))

# NU
#               x:
def Nu(x):
    y = x/2
    return (1/y)*(norm.cdf(y)-.5)/(y*norm.cdf(y)+norm.pdf(y))


# PVAL1_SUB_1
#               N:   the total number of nodes
#               b:   Zmax
#               r:
#               x:
#           lower:
#           upper:
def pval1_sub1(N, b, r, x, lower, upper):
    if b < 0: return 1
    theta_b = np.zeros(N-1)
    pos = np.where((1+(2*r*b)) > 0)[0]
    theta_b[pos] = (np.sqrt((1+(2*r*b))[pos])-1)/r[pos]
    theta_b = np.nan_to_num(theta_b)
    ratio = np.exp((b-theta_b)**2/2 + r*theta_b**3/6)/np.sqrt(1+r*theta_b)
    a = x*Nu(np.sqrt(2*b**2*x))*ratio
    nn_l = np.int64(np.ceil(N/2))-(np.where(1+2*r[np.arange(np.int64(np.ceil(N/2)))]*b>0)[0]).size
    nn_r = np.int64(np.ceil(N/2))-(np.where(1+2*r[np.arange(np.int64(np.ceil(N/2)), (N-1))]*b>0)[0]).size
    if (nn_l > .35*N) or (nn_r > .35*N): return 0
    if nn_l >= lower:
        neg = np.where(1+2*r[np.arange(np.int64(np.ceil(N/2)))]*b<=0)[0]
        dif = np.concatenate((np.diff(neg), N/2-nn_l))
        id1 = np.argmax(dif)
        id2 = id1+np.int64(np.ceil(.03*N))
        id3 = id2+np.int64(np.ceil(.09*N))
        inc = (a[id3]-a[id2])/(id3-id2)
        a[np.arange(id2)[::-1]] = a[id2+1]-inc*(np.arange(id2))
    if nn_r >= (N-upper):
        neg = np.where(1+2*r[np.arange(np.int64(np.ceil(N/2)), N-1)]*b<=0)[0]
        id1 = np.amin(np.concatenate((neg+np.int64(np.ceil(N/2))-2, [np.int64(np.ceil(N/2))-2])))
        id2 = id1-np.int64(np.ceil(.03*N))
        id3 = id2-np.int64(np.ceil(.09*N))
        inc = (ratio[id3]-ratio[id2])/(id3-id2)
        ratio[np.arange(id2, (N-1))] = ratio[id2-1]+inc*((np.arange(id2, (N-1)))-id2)
        ratio[ratio < 0] = 0
        a[np.arange(np.int64((N/2-1)), (N-1))] = (x*Nu(np.sqrt(2*b**2*x))*ratio)[np.arange(np.int64((N/2-1)), (N-1))]
    a[a < 0] = 0
    return 2*norm.pdf(b)*b*integrate.quad(lambda s, arr=a: arr[np.int64(s)], a=lower, b=upper, limit=3000, epsabs=0.0001220703, epsrel=0.0001220703)[0]
    
# PVAL1_SUB2
#               N:   the total number of nodes
#               b:   Zmax
#               r:
#               x:
#           lower:
#           upper:
def pval1_sub2(N, b, r, x, lower, upper):
    if b < 0: return 1
    theta_b = np.zeros(N-1)
    pos = np.where((1+(2*r*b)) > 0)[0]
    theta_b[pos] = (np.sqrt((1+(2*r*b))[pos])-1)/r[pos]
    ratio = np.exp((b-theta_b)**2/2+r*theta_b**3/6)/np.sqrt(1+r*theta_b)
    a = x*Nu(np.sqrt(2*b**2*x))*ratio
    a = np.nan_to_num(a)
    nn = N-1-pos.size
    if nn > .75*N: return 0
    if nn >= ((lower-1)+(N-upper)):
        neg = np.where((1+(2*r*b))<=0)[0]
        dif = neg[1:nn]-neg[:(nn-1)]
        id1 = np.argmax(dif)
        id2 = id1+np.int64(np.ceil(.03*N))
        id3 = id2+np.int64(np.ceil(.09*N))
        inc = (a[id3]-a[id2])/(id3-id2)
        a[np.arange(id2)[::-1]] = a[id2+1]-inc*np.arange(id2)
        a[np.arange((np.int64(N/2)+1), N)] = a[np.arange(np.int64(N/2))[::-1]]
        a = np.nan_to_num(a)
        a[a < 0] = 0
    return norm.pdf(b)*b*integrate.quad(lambda s, arr=a: arr[np.int64(s)], a=lower, b=upper, limit=3000)[0]
        

# PERMPVAL1
def permval1(N, connectivity, scanZ, statistic="all", B=100, n0=None, n1=None):
    n0 = np.int64(np.ceil(.05*N)) if n0 is None else np.int64(np.ceil(n0))
    n1 = np.int64(np.floor(.95*N)) if n1 is None else np.int64(np.floor(n1))
    original_Z = np.zeros(B*N).reshape((B, N))
    weighted_Z = np.zeros(B*N).reshape((B, N))
    max_type_Z = np.zeros(B*N).reshape((B, N))
    generalized_Z = np.zeros(B*N).reshape((B, N))
    index = np.arange(N, dtype="int64")
    for b in np.arange(B):
        np.random.shuffle(index)
        permmatch = np.zeros(N, dtype="int64")
        for i in np.arange(N):
            permmatch[index[i]] = i
        connectivity_star = []
        for i in np.arange(N):
            oldlinks = connectivity[permmatch[i]]
            connectivity_star.append(index[oldlinks])
        changepoint_star = changepoint1(connectivity_star, N, statistic, n0, n1)
        if statistic in ["all", "original", "ori", "o"]:
            original_Z[b] = changepoint_star["original"]["Z"]
        if statistic in ["all", "weighted", "wei", "w"]:
            weighted_Z[b] = changepoint_star["weighted"]["Zw"]
        if statistic in ["all", "max", "m"]:
            max_type_Z[b] = changepoint_star["max_type"]["M"]
        if statistic in ["all", "generalized", "gen", "g"]:
            generalized_Z[b] = changepoint_star["generalized"]["S"]
    output = {}
    p = 1-(np.arange(B))/B
    if statistic in ["all", "original", "ori", "o"]:
        maxZ = np.amax(original_Z[::, n0:(n1+1)], axis=1)
        maxZs = np.sort(maxZ)
        output["original"] = {"pval" : np.average(maxZs >= scanZ["original"]["Zmax"]),
                              "curve" : np.stack((maxZs, p), axis=1), "maxZs" : maxZs, "Z" : original_Z[b]}
    if statistic in ["all", "weighted", "wei", "w"]:
        maxZ = np.amax(weighted_Z[::, n0:(n1+1)], axis=1)
        maxZs = np.sort(maxZ)
        output["weighted"] = {"pval" : np.average(maxZs >= scanZ["weighted"]["Zmax"]),
                              "curve" : np.stack((maxZs, p), axis=1), "maxZs" : maxZs, "Z" : weighted_Z[b]}
    if statistic in ["all", "max", "m"]:
        maxZ = np.amax(max_type_Z[::, n0:(n1+1)], axis=1)
        maxZs = np.sort(maxZ)
        output["max_type"] = {"pval" : np.average(maxZs >= scanZ["max_type"]["Zmax"]),
                              "curve" : np.stack((maxZs, p), axis=1), "maxZs" : maxZs, "Z" : max_type_Z[b]}
    if statistic in ["all", "generalized", "gen", "g"]:
        maxZ = np.amax(generalized_Z[::, n0:(n1+1)], axis=1)
        maxZs = np.sort(maxZ)
        output["generalized"] = {"pval" : np.average(maxZs >= scanZ["generalized"]["Zmax"]),
                                 "curve" : np.stack((maxZs, p), axis=1), "maxZs" : maxZs, "Z" : generalized_Z[b]}
    return output


# PVAL1
#               N:   the total number of nodes
#               E:   the edge matrix for the similarity graph
# connectivity[i]:   the list of nodes that are connected to i by an edge
#           scanZ:
#       statistic:   the scan statistics to be computed - a string indicating the type of scan statistic desired
#                    the default is "all"
#                    "all"                 - specifies all of the scan statistics (original, weighted, generalized, max-type)
#                    "o" or "original"     - specifies the original edge-count scan statistic
#                    "w" or "weighted"     - specifies the weighted edge-count scan statistic
#                    "g" or "generalized"  - specifies the generalized edge-count scan statistic
#                    "m" or "max"          - specifies the max-type edge-count scan statistic
#       skew_corr:   if True, the p-value approximation will incorporate skewness correction
#           lower:
#           upper:
def pval1(E, N, connectivity, scanZ, statistic="all", skew_corr=True, lower=None, upper=None):
    lower = np.int64(np.ceil(.05*N)) if lower is None else lower
    upper = np.int64(np.floor(.95*N)) if upper is None else upper
    output = {} # define an empty container to store the results
    edge_list = np.stack(np.nonzero(np.tril(E, k=-1))[::-1], axis=1) # get the edge list
    degrees = np.array([len(node) for node in connectivity]) # get the degree of each node
    sum_degrees_squared = np.sum(degrees**2) # calculate the sum of the squared degrees
    n_edges = np.int64(np.sum(degrees)/2) # calculate the number of edges in the similarity graph
    if skew_corr == False:
        if statistic in ["all", "original", "ori", "o"]:
            b = scanZ["original"]["Zmax"]
            if b > 0:
                def integrand_O(s):
                    x = rho1(N, s, n_edges, sum_degrees_squared)
                    return x*Nu(np.sqrt(2*b**2*x))
                pval_original = norm.pdf(b)*b*integrate.quad(integrand_O, a=lower, b=upper)[0]
            else:
                pval_original = 1
            output["original"] = np.amin(np.concatenate(([pval_original], [1])))
        if statistic in ["all", "weighted", "wei", "w"]:
            b = scanZ["weighted"]["Zmax"]
            if b > 0:
                def integrand_W(t):
                    x = rho1_Rw(N, t)
                    return x*Nu(np.sqrt(2*b**2*x))
                pval_weighted = norm.pdf(b)*b*integrate.quad(integrand_W, a=lower, b=upper)[0]
            else:
                pval_weighted = 1
            output["weighted"] = np.amin(np.concatenate(([pval_weighted], [1])))
        if statistic in ["all", "max", "m"]:
            b = scanZ["max_type"]["Zmax"]
            if b > 0:
                def integrand1(t):
                    x1 = N/(2*t*(N-t))
                    return x1*Nu(np.sqrt(2*b**2*x2))
                def integrand2(t):
                    x2 = rho1_Rw(N, t)
                    return x2*Nu(np.sqrt(2*b**2*x2))
                pval_u1 = 2*norm.pdf(b)*b*integrate.quad(integrand1, a=lower, b=upper)[0]
                pval_u2 = norm.pdf(b)*b*integrate.quad(integrand2, a=lower, b=upper)[0]
                pval_maxtype = 1-(1-np.amin(np.concatenate(([pval_u1], [1]))))*(1-np.amin(np.concatenate(([pval_u2], [1]))))
            else:
                pval_maxtype = 1
            output["max_type"] = pval_maxtype
        if statistic in ["all", "generalized", "gen", "g"]:
            b = scanZ["generalized"]["Zmax"]
            if b > 0:
                def integrand_G(t, w):
                    x1 = N/(2*t*(N-t))
                    x2 = rho1_Rw(N, t)
                    return 2*(x1*np.cos(w)**2+x2*np.sin(w)**2)*b*Nu(np.sqrt(2*b*(x1*np.cos(w)**2+x2*np.sin(w)**2)))/(2*np.pi)
                pval_generalized = chi2.pdf(b, 2)*integrate.dblquad(integrand_G, a=0, b=2*np.pi, gfun=lower, hfun=upper)[0]
            else:
                pval_generalized = 1
            output["generalized"] = np.amin(np.concatenate(([pval_generalized], [1])))
        return ouput
    x1 = np.sum(degrees*(degrees-1))
    x2 = np.sum(degrees*(degrees-1)*(degrees-2))
    x3 = 0
    for i in np.arange(edge_list.shape[0]):
        x3 = x3+(degrees[edge_list[i, 0]]-1)*(degrees[edge_list[i, 1]]-1)
    x4 = np.sum(degrees*(degrees-1)*(n_edges-degrees))
    x5 = 0
    for i in np.arange(edge_list.shape[0]):
        j = edge_list[i, 0]
        k = edge_list[i, 1]
        x5 = x5+np.sum(np.isin(connectivity[j], connectivity[k]))
    if statistic in ["all", "original", "ori", "o"]:
        b = scanZ["original"]["Zmax"]
        if b > 0:
            s = np.arange(1, N+1)
            x = rho1(N, s, n_edges, sum_degrees_squared)
            p1 = 2*s*(N-s)/(N*(N-1))
            p2 = 4*s*(s-1)*(N-s)*(N-s-1)/(N*(N-1)*(N-2)*(N-3))
            p3 = s*(N-s)*((N-s-1)*(N-s-2)+(s-1)*(s-2))/(N*(N-1)*(N-2)*(N-3))
            p4 = 8*s*(s-1)*(s-2)*(N-s)*(N-s-1)*(N-s-2)/(N*(N-1)*(N-2)*(N-3)*(N-4)*(N-5))
            mu = p1*n_edges
            sig = np.sqrt(np.amax(np.stack((p2*n_edges+(p1/2-p2)*sum_degrees_squared+(p2-p1**2)*n_edges**2, np.zeros(N)), axis=1),
                                  axis=1))
            ER3 = p1*n_edges+p1/2*3*x1+p2*(3*n_edges*(n_edges-1)-3*x1)+p3*x2+p2/2*(3*x4-6*x3)+\
                  p4*(n_edges*(n_edges-1)*(n_edges-2)-x2-3*x4+6*x3)-2*p4*x5
            r = (mu**3+3*mu*sig**2-ER3)/sig**3
            theta_b = np.zeros(N)
            pos = np.where((1+(2*r*b)) > 0)[0]
            theta_b[pos] = (np.sqrt((1+(2*r*b))[pos])-1)/r[pos]
            ratio = np.exp((b-theta_b)**2/2+r*theta_b**3/6)/np.sqrt(1+r*theta_b)
            a = x*Nu(np.sqrt(2*b**2*x))*ratio
            nn = N-pos.size-1
            if nn > .75*N:
                def integrand(s):
                    x = rho1(N, s, n_edges, sum_degrees_squared)
                    return x*Nu(np.sqrt(2*b**2*x))
                pval_original = norm.pdf(b)*b*integrate.quad(integrand, a=lower, b=upper, limit=3000)[0]
                output["original"] = np.amin(np.concatenate(([pval_original], [1])))
            else:
                if nn >= ((lower-1)+(N-upper)):
                    neg = np.where((1+(2*r*b)) <= 0)[0]
                    dif = neg[np.arange(1, nn)]-neg[np.arange(nn-1)]
                    id1 = np.argmax(dif)
                    id2 = id1+np.int64(np.ceil(.03*N))
                    id3 = id2+np.int64(np.ceil(.09*N))
                    inc = (a[id3]-a[id2])/(id3-id2)
                    a[np.arange(id2+1)[::-1]] = a[id2+1]-inc*np.arange(1, id2+2)
                    a[np.arange(np.int64(np.ceil(N/2)), N)] = a[np.arange(np.int64(N/2))[::-1]]
                    a[a < 0] = 0
                pval_original = norm.pdf(b)*b*integrate.quad(lambda s, arr=a: a[np.int64(s)], a=lower, b=upper, limit=3000)[0]
                if not np.isnan(pval_original):
                    output["original"]=np.amin(np.concatenate(([pval_original], [1])))
                else:
                    def integrand(s):
                        x = rho1(N, s, n_edges, sum_degrees_squared)
                        return x*Nu(np.sqrt(2*b**2*x))
                    pval_original = norm.pdf(b)*b*integrate.quad(integrand, a=lower, b=upper)[0]
                    output["original"]=np.amin(np.concatenate(([pval_original], [1])))
        else:
            output["original"]=1
            import
            import
            
    if statistic in ["all", "weighted", "wei", "w", "max", "m"]:
        t = np.arange(1, N, dtype="float")
        A1 = n_edges*t*(t-1)/(N*(N-1))+3*x1*t*(t-1)*(t-2)/(N*(N-1)*(N-2))+\
             (3*n_edges*(n_edges-1)-3*x1)*t*(t-1)*(t-2)*(t-3)/(N*(N-1)*(N-2)*(N-3))+\
             x2*t*(t-1)*(t-2)*(t-3)/(N*(N-1)*(N-2)*(N-3))+(6*x3-6*x5)*(t*(t-1)*(t-2)*(t-3))/(N*(N-1)*(N-2)*(N-3))+\
             2*x5*(t*(t-1)*(t-2))/(N*(N-1)*(N-2))+(3*x4+6*x5-12*x3)*t*(t-1)*(t-2)*(t-3)*(t-4)/(N*(N-1)*(N-2)*(N-3)*(N-4))+\
             (n_edges*(n_edges-1)*(n_edges-2)+6*x3-2*x5-x2-3*x4)*t*(t-1)*(t-2)*(t-3)*(t-4)*(t-5)/(N*(N-1)*(N-2)*(N-3)*(N-4)*(N-5))
        B1 = (n_edges*(n_edges-1)-x1)*(t*(t-1)*(N-t)*(N-t-1))/(N*(N-1)*(N-2)*(N-3))+\
             (x4+2*x5-4*x3)*(t*(t-1)*(t-2)*(N-t)*(N-t-1))/(N*(N-1)*(N-2)*(N-3)*(N-4))+\
             (n_edges*(n_edges-1)*(n_edges-2)+\
             6*x3-2*x5-x2-3*x4)*t*(t-1)*(t-2)*(t-3)*(N-t)*(N-t-1)/(N*(N-1)*(N-2)*(N-3)*(N-4)*(N-5))
        C1 = (n_edges*(n_edges-1)-x1)*(N-t)*(N-t-1)*t*(t-1)/(N*(N-1)*(N-2)*(N-3))+\
             (x4+2*x5-4*x3)*(N-t)*(N-t-1)*(N-t-2)*t*(t-1)/(N*(N-1)*(N-2)*(N-3)*(N-4))+\
             (n_edges*(n_edges-1)*(n_edges-2)+\
             6*x3-2*x5-x2-3*x4)*t*(t-1)*(N-t)*(N-t-1)*(N-t-2)*(N-t-3)/(N*(N-1)*(N-2)*(N-3)*(N-4)*(N-5))
        D1 = n_edges*(N-t)*(N-t-1)/(N*(N-1))+3*x1*(N-t)*(N-t-1)*(N-t-2)/(N*(N-1)*(N-2))+\
             (3*n_edges*(n_edges-1)-3*x1)*(N-t)*(N-t-1)*(N-t-2)*(N-t-3)/(N*(N-1)*(N-2)*(N-3))+\
             x2*(N-t)*(N-t-1)*(N-t-2)*(N-t-3)/(N*(N-1)*(N-2)*(N-3))+\
             (6*x3-6*x5)*((N-t)*(N-t-1)*(N-t-2)*(N-t-3))/(N*(N-1)*(N-2)*(N-3))+\
             2*x5*((N-t)*(N-t-1)*(N-t-2))/(N*(N-1)*(N-2))+\
             (3*x4+6*x5-12*x3)*(N-t)*(N-t-1)*(N-t-2)*(N-t-3)*(N-t-4)/(N*(N-1)*(N-2)*(N-3)*(N-4))+\
             (n_edges*(n_edges-1)*(n_edges-2)+\
             6*x3-2*x5-x2-3*x4)*(N-t)*(N-t-1)*(N-t-2)*(N-t-3)*(N-t-4)*(N-t-5)/(N*(N-1)*(N-2)*(N-3)*(N-4)*(N-5))
        r1 = n_edges*(t*(t-1)/(N*(N-1)))+2*(0.5*sum_degrees_squared-n_edges)*t*(t-1)*(t-2)/(N*(N-1)*(N-2))+\
             (n_edges*(n_edges-1)-(2*(0.5*sum_degrees_squared-n_edges)))*t*(t-1)*(t-2)*(t-3)/(N*(N-1)*(N-2)*(N-3))
        r2 = n_edges*((N-t)*(N-t-1)/(N*(N-1)))+2*(0.5*sum_degrees_squared-n_edges)*(N-t)*(N-t-1)*(N-t-2)/(N*(N-1)*(N-2))+\
             (n_edges*(n_edges-1)-(2*(0.5*sum_degrees_squared-n_edges)))*(N-t)*(N-t-1)*(N-t-2)*(N-t-3)/(N*(N-1)*(N-2)*(N-3))
        r12 = (n_edges*(n_edges-1)-(2*(0.5*sum_degrees_squared-n_edges)))*t*(t-1)*(N-t)*(N-t-1)/(N*(N-1)*(N-2)*(N-3))
        x = rho1_Rw(N, t)
        q = (N-t-1)/(N-2)
        p = (t-1)/(N-2)
        mu = n_edges*(q*t*(t-1)+p*(N-t)*(N-t-1))/(N*(N-1))
        sig1 = q**2*r1+2*q*p*r12+p**2*r2-mu**2
        sig = np.sqrt(sig1)
        ER3 = q**3*A1+3*q**2*p*B1+3*q*p**2*C1+p**3*D1
        r = (ER3-3*mu*sig**2-mu**3)/sig**3
        r_Rw = r
        x_Rw = x
        if statistic in ["all", "weighted", "wei", "w"]:
            b = scanZ["weighted"]["Zmax"]
            result_u2 = pval1_sub2(N, b, r, x, lower, upper)
            if result_u2 > 0:
                output["weighted"] = np.amin(np.concatenate(([result_u2], [1])))
            else:
                if b > 0:
                    def integrand_W(t):
                        x = rho1_Rw(N, t)
                        return x*Nu(np.sqrt(2*b**2*x))
                    pval_weighted = norm.pdf(b)*b*integrate.quad(integrand_W, lower, upper)[0]
                else:
                    pval_weighted = 1
                output["weighted"] = np.amin(np.concatenate(([pval_weighted], [1])))
        if statistic in ["all", "max", "m"]:
            b = scanZ["max_type"]["Zmax"]
            x = N/(2*t*(N-t))
            q = 1
            p = -1
            mu = n_edges*(q*t*(t-1)+p*(N-t)*(N-t-1))/(N*(N-1))
            sig1 = q**2*r1+2*q*p*r12+p**2*r2-mu**2
            sig = np.sqrt(np.amax(np.stack((sig1, np.zeros(N-1)), axis=1), axis=1))
            ER3 = q**3*A1+3*q**2*p*B1+3*q*p**2*C1+p**3*D1
            r = (ER3-3*mu*sig**2-mu**3)/sig**3
            result_u1 = pval1_sub1(N, b, r, x, lower, upper)
            result_u2 = pval1_sub2(N, b, r_Rw, x_Rw, lower, upper)
            if (not result_u1 > 0) or (not result_u2 > 0):
                if b > 0:
                    def integrand1(t):
                        x1 = N/(2*t*(N-t))
                        return x1*Nu(np.sqrt(2*b**2*x1))
                    def integrand2(t):
                        x2 = rho1_Rw(N, t)
                        return x2*Nu(np.sqrt(2*b**2*x2))
                    pval_u1 = 2*norm.pdf(b)*b*integrate.quad(integrand1, lower, upper)[0]
                    pval_u2 = norm.pdf(b)*b*integrate.quad(integrand2, lower, upper)[0]
                    pval_maxtype = 1-(1-np.amin(np.concatenate(([pval_u1], [1]))))*(1-np.amin(np.concatenate(([pval_u2], [1]))))
                else:
                    pval_maxtype = 1
                output["max_type"] = pval_maxtype
            else:
                output["max_type"] = 1-(1-np.amin(np.concatenate(([result_u1], [1]))))*(1-np.amin(np.concatenate(([result_u2], [1]))))
    if statistic in ["all", "generalized", "gen", "g"]:
        b = scanZ["generalized"]["Zmax"]
        if b > 0:
            def integrand_G(t, w):
                x1 = N/(2*t*(N-t))
                x2 = rho1_Rw(N, t)
                return 2*(x1*np.cos(w)**2+x2*np.sin(w)**2)*b*Nu(np.sqrt(2*b*(x1*np.cos(w)**2+x2*np.sin(w)**2)))/(2*np.pi)
            pval_generalized = chi2.pdf(b, 2)*integrate.dblquad(integrand_G, a=0, b=2*np.pi, gfun=lower, hfun=upper)[0]
        else:
            pval_generalized = 1
        output["generalized"] = np.amin(np.concatenate(([pval_generalized], [1])))
    return output


# CHANGEPOINT1
# connectivity[i]:   the list of nodes that are connected to i by an edge
#               N:   the total number of nodes
#       statistic:   the scan statistics to be computed - a string indicating the type of scan statistic desired
#                    the default is "all"
#                    "all"                - specifies all of the scan statistics (original, weighted, generalized, max-type)
#                    "o" or "original"    - specifies the original edge-count scan statistic
#                    "w" or "weighted"    - specifies the weighted edge-count scan statistic
#                    "g" or "generalized" - specifies the generalized edge-count scan statistic
#                    "m" or "max"         - specifies the max-type edge-count scan statistic
#              n0:   the starting index to be considered as a candidate for the change-point
#              n1:   the ending index to be considered as a candidate for the change-point
def changepoint1(connectivity, N, statistic="all", n0=None, n1=None):
    # define default values for n0 and n1, which are functions of N
    n0 = np.int64(np.ceil(.05*N)) if n0 is None else np.int64(np.ceil(n0))
    n1 = np.int64(np.floor(.95*N)) if n1 is None else np.int64(np.floor(n1))
    
    # get the degree of each node
    degrees = np.array([len(node) for node in connectivity])
    
    # calculate the sum of the squared degrees
    sum_degrees_squared = np.sum(degrees**2)
    
    # calculate the number of edges in the similarity graph
    n_edges = np.int64(np.sum(degrees)/2)
    
    # define storage containers
    g = np.ones(N, dtype="int64")
    R = np.zeros(N, dtype="int64")
    R1 = np.zeros(N, dtype="int64")
    R2 = np.zeros(N, dtype="int64")
    
    for i in np.arange(N-1, dtype="int64"):
        g[i] = np.int64(0)
        links = connectivity[i]
        
        if i == 0:
            if links.size > 0:
                R[i] = np.sum(np.tile(g[i], links.size) != g[links])
            else:
                R[i] = np.int64(0)
            R1[i] = np.int64(0)
            R2[i] = n_edges-links.size
        else:
            if links.size > 0:
                add = np.sum(np.tile(g[i], links.size) != g[links])
                subtract = links.size-add
                R[i] = R[(i-1)]+add-subtract
                R1[i] = R1[(i-1)]+subtract
            else:
                R[i] = R[(i-1)]
                R1[i] = R1[(i-1)]
        R2[i] = n_edges-R[i]-R1[i]
    
    tt = np.arange(1, N+1, dtype="int64")
    temp = np.arange(n0, n1, dtype="int64")
    
    scanZ = {}
    if statistic in ["all", "original", "ori", "o"]:
        mu_t = n_edges*2*tt*(N-tt)/(N*(N-1))
        p1_tt = 2*tt*(N-tt)/(N*(N-1))
        p2_tt = tt*(N-tt)*(N-2)/(N*(N-1)*(N-2))
        p3_tt = 4*tt*(N-tt)*(tt-1)*(N-tt-1)/(N*(N-1)*(N-2)*(N-3))
        A_tt = (p1_tt-2*p2_tt+p3_tt)*n_edges+(p2_tt-p3_tt)*sum_degrees_squared+p3_tt*n_edges**2
        Z = (mu_t-R)/np.sqrt(A_tt-mu_t**2)
        Z[N-1] = 0
        
        tauhat = temp[np.argmax(Z[n0:n1])]
        original = {"tauhat" : tauhat, "Zmax" : Z[tauhat], "Z" : Z, "R" : R}
        scanZ["original"] = original
        
    if statistic in ["all", "generalized", "gen", "g", "weighted", "wei", "w", "max", "m"]:
        Rw = ((N-tt-1)*R1+(tt-1)*R2)/(N-2)
        mu_Rw = n_edges*((N-tt-1)*tt*(tt-1)+(tt-1)*(N-tt)*(N-tt-1))/(N*(N-1)*(N-2))
        mu_R1 = n_edges*tt*(tt-1)/(N*(N-1))
        mu_R2 = n_edges*(N-tt)*(N-tt-1)/(N*(N-1))
        
        v11 = mu_R1*(1-mu_R1)+2*(.5*sum_degrees_squared-n_edges)*(tt*(tt-1)*(tt-2))/(N*(N-1)*(N-2))+\
              (n_edges*(n_edges-1)-2*(.5*sum_degrees_squared-n_edges))*(tt*(tt-1)*(tt-2)*(tt-3))/(N*(N-1)*(N-2)*(N-3))
        v22 = mu_R2*(1-mu_R2)+2*(.5*sum_degrees_squared-n_edges)*((N-tt)*(N-tt-1)*(N-tt-2))/(N*(N-1)*(N-2))+\
              (n_edges*(n_edges-1)-2*(.5*sum_degrees_squared-n_edges))*((N-tt)*(N-tt-1)*(N-tt-2)*(N-tt-3))/(N*(N-1)*(N-2)*(N-3))
        v12 = (n_edges*(n_edges-1)-2*(.5*sum_degrees_squared-n_edges))*tt*(N-tt)*(tt-1)*(N-tt-1)/(N*(N-1)*(N-2)*(N-3))-mu_R1*mu_R2
        varRw = (((N-tt-1)/(N-2))**2)*v11+2*((N-tt-1)/(N-2))*((tt-1)/(N-2))*v12+(((tt-1)/(N-2))**2)*v22
        Zw = -(mu_Rw-Rw)/np.sqrt(np.amax(np.stack((varRw, np.zeros(N)), axis=1), axis=1))
        
        if statistic in ["all", "weighted", "wei", "max" "m"]:
            tauhat = temp[np.argmax(Zw[n0:n1])]
            weighted = {"tauhat" : tauhat, "Zmax" : Zw[tauhat], "Zw" : Zw, "Rw" : Rw}
            scanZ["weighted"] = weighted
            
        if statistic in ["all", "generalized", "gen", "g", "max", "m"]:
            Rd = R1-R2
            Zd = (Rd-(mu_R1-mu_R2))/np.sqrt(np.amax(np.stack((v11+v22-2*v12, np.zeros(N)), axis=1), axis=1))
            
            if statistic in ["all", "max", "m"]:
                M = np.amax(np.stack((np.absolute(Zd), Zw), axis=1), axis=1)
                tauhat = temp[np.argmax(M[n0:n1])]
                max_type = {"tauhat" : tauhat, "Zmax" : M[tauhat], "M" : M}
                scanZ["max_type"] = max_type
                
            if statistic in ["all", "generalized", "gen", "g"]:
                Z = Zw**2+Zd**2
                tauhat = temp[np.argmax(Z[n0:n1])]
                generalized = {"tauhat" : tauhat, "Zmax" : Z[tauhat], "S" : Z}
                scanZ["generalized"] = generalized
    
    return scanZ
    


# GSEG1
#          N:   the number of observations (nodes in the sequence)
#          E:   the edge matrix for the similarity graph
#  statistic:   the scan statistics to be computed - a string indicating the type of scan statistic desired
#               the default is "all"
#               "all"                 - specifies all of the scan statistics (original, weighted, generalized, max-type)
#               "o" or "original"     - specifies the original edge-count scan statistic
#               "w" or "weighted"     - specifies the weighted edge-count scan statistic
#               "g" or "generalized"  - specifies the generalized edge-count scan statistic
#               "m" or "max"          - specifies the max-type edge-count scan statistic
#         n0:   the starting index to be considered as a candidate for the change-point
#         n1:   the ending index to be considered as a candidate for the change-point
#  pval_appr:   if True, the function returns p-value approximation based on asymptotic properties
#  skew_corr:   (only when pval.appr=True) if True, the p-value approximation will incorporate skewness correction
#  pval_perm:   if True, the function returns p-values from doing B permutations
#          B:   (only when pval.perm=True) the number of iterations to run with permutation
def gseg1(E, N, statistic="all", n0=None, n1=None, pval_asym=True, skew_corr=True, pval_perm=False, B=100):
    # define default values for n0 and n1, which are functions of N
    if n0 is None:
        n0 = np.int64(np.ceil(.05*N))
    elif n0 < 2:
        n0 = np.int64(2)
    else:
        n0 = np.int64(np.ceil(n0))
    
    if n1 is None:
        n1 = np.int64(np.floor(.95*N))
    elif n1 > (N-2):
        n1 = np.int64(N-2)
    else:
        n1 = np.int64(np.floor(n1))
    
    # create a storage container for the results
    r1 = {}
    
    # create a connectivity list
    # that is, connectivity[i] is the numpy array of nodes that are connected to node i by an edge
    connectivity = []
    for i in np.arange(N):
        connectivity.append(np.nonzero(E[i])[0])
    
    r1["scanZ"] = changepoint1(connectivity = connectivity, N=N, statistic=statistic, n0=n0, n1=n1)
    
    # get the p-values
    if pval_asym == True:
        r1["pval_asym"] = pval1(E=E, N=N, connectivity=connectivity, scanZ=r1["scanZ"],
                                statistic=statistic, skew_corr=skew_corr, lower=n0, upper=n1)
    if pval_perm == True:
        r1["pval_perm"] = permval1(N=N, connectivity=connectivity, scanZ=r1["scanZ"],
                                   statistic=statistic, B=100, n0=n0, n1=n1)
    return r1



# CHANGEPOINT2
# connectivity[i]:   the list of nodes that are connected to i by an edge
#               N:   the total number of nodes
#       statistic:   the scan statistics to be computed - a string indicating the type of scan statistic desired
#                    the default is "all"
#                    "all"                - specifies all of the scan statistics (original, weighted, generalized, max-type)
#                    "o" or "original"    - specifies the original edge-count scan statistic
#                    "w" or "weighted"    - specifies the weighted edge-count scan statistic
#                    "g" or "generalized" - specifies the generalized edge-count scan statistic
#                    "m" or "max"         - specifies the max-type edge-count scan statistic
#              n0:   the starting index to be considered as a candidate for the change-point
#              n1:   the ending index to be considered as a candidate for the change-point
def changepoint2(connectivity, N, statistic="all", n0=None, n1=None):
    # define default values for n0 and n1, which are functions of N
    n0 = np.int64(np.ceil(.05*N)) if n0 is None else np.int64(np.ceil(n0))
    n1 = np.int64(np.floor(.95*N)) if n1 is None else np.int64(np.floor(n1))
    
    # get the degree of each node
    degrees = np.array([len(node) for node in connectivity])
    
    # calculate the sum of the squared degrees
    sum_degrees_squared = np.sum(degrees**2)
    
    # calculate the number of edges in the similarity graph
    n_edges = np.int64(np.sum(degrees)/2)
    
    # define storage containers
    Rtmp = np.zeros(N*N).reshape((N, N))
    R1 = np.zeros(N*N).reshape((N, N))
    R2 = np.zeros(N*N).reshape((N, N))
    Rw = np.zeros(N*N).reshape((N, N))
    
    for i in np.arange(N-1, dtype="int64"):
        g = np.zeros(N)
        for j in np.arange((i+1), N, dtype="int64"):
            g[j] = 1
            links = connectivity[j]
            if j == (i+1):
                if links.size > 0:
                    Rtmp[i, j] = np.sum(np.tile(g[j], links.size) != g[links])
                    R1[i, j] = 0
                    R2[i, j] = n_edges-links.size
            else:
                if links.size > 0:
                    add = np.sum(np.tile(g[j], links.size) != g[links])
                    subtract = links.size-add
                    Rtmp[i, j] = Rtmp[i, (j-1)]+add-subtract
                    R1[i, j] = R1[i, (j-1)]+subtract
                else:
                    Rtmp[i, j] = Rtmp[i, (i-j)]
                    R1[i, j] = R1[i, (j-1)]
            R2[i, j] = n_edges-Rtmp[i, j]-R1[i, j]
            Rw[i, j] = ((N-j+i-1)/(N-2))*R1[i, j]+(j-i-1)/(N-2)*R2[i, j]
    dif = np.zeros(N*N).reshape((N, N))
    for i in np.arange(1, N+1):
        for j in np.arange(1, N+1):
            dif[i-1, j-1] = j-i
    difv = dif.flatten(order="C").astype("int64")
    ids = np.where(difv > 0)[0]
    difv = difv-1
    ids2 = np.where(np.logical_and(difv >= n0, difv <= n1))[0]
    
    scanZ = {}
    if statistic in ["all", "original", "ori", "o"]:
        tt = np.arange(1, (N+1), dtype="int64")
        mu_t = n_edges*2*tt*(N-tt)/(N*(N-1))
        p1_tt = 2*tt*(N-tt)/(N*(N-1))
        p2_tt = 4*tt*(N-tt)*(tt-1)*(N-tt-1)/(N*(N-1)*(N-2)*(N-3))
        V_tt = p2_tt*n_edges+(p1_tt/2-p2_tt)*sum_degrees_squared+(p2_tt-p1_tt**2)*n_edges**2
        Rv = Rtmp.flatten(order="C")
        Zv = np.zeros(N*N)
        Zv[ids] = (mu_t[difv[ids]]-Rv[ids])/np.sqrt(V_tt[difv[ids]])
        Zmax = np.amax(Zv[ids2])
        tauhat0 = np.where(Zv == Zmax)[0]
        tauhat = np.zeros((tauhat0.size, 2), dtype=np.int_)
        for i in np.arange(tauhat0.size):
            tauhat[i, 0] = np.int_(np.floor(tauhat0[i]/N))
            tauhat[i, 1] = np.int_(np.ceil(tauhat0[i]-1)%N+1)
        # tauhat = np.array([np.floor(tauhat0/N), np.ceil(tauhat0-1)%N+1], dtype="int64")
        original = {"tauhat" : tauhat, "Zmax" : Zmax, "Z" : Zv.reshape((N, -1)), "R" : Rtmp}
        scanZ["original"] = original
        
    if statistic in ["all", "generalized", "gen", "g", "weighted", "wei", "w", "max", "m"]:
        if n0 <= 1:
            n0 = 1
        if n1 >= (N-1):
            n1 = N-3
        ids2 = np.where(np.logical_and(difv >= n0, difv <= n1))[0]
        tt = np.arange(1, (N+1), dtype="int64")
        mu_r1 = n_edges*tt*(tt-1)/(N*(N-1))
        mu_r2 = n_edges*(N-tt)*(N-tt-1)/(N*(N-1))
        sig11 = mu_r1*(1-mu_r1)+2*(0.5*sum_degrees_squared-n_edges)*(tt*(tt-1)*(tt-2))/(N*(N-1)*(N-2))+(n_edges*(n_edges-1)-2*(0.5*sum_degrees_squared-n_edges))*(tt*(tt-1)*(tt-2)*(tt-3))/(N*(N-1)*(N-2)*(N-3))
        sig22 = mu_r2*(1-mu_r2)+2*(0.5*sum_degrees_squared-n_edges)*((N-tt)*(N-tt-1)*(N-tt-2))/(N*(N-1)*(N-2))+(n_edges*(n_edges-1)-2*(0.5*sum_degrees_squared-n_edges))*((N-tt)*(N-tt-1)*(N-tt-2)*(N-tt-3))/(N*(N-1)*(N-2)*(N-3))
        sig12 = (n_edges*(n_edges-1)-2*(0.5*sum_degrees_squared-n_edges))*tt*(N-tt)*(tt-1)*(N-tt-1)/(N*(N-1)*(N-2)*(N-3))-mu_r1*mu_r2
        sig21 = sig12
        p = (tt-1)/(N-2)
        q = 1-p
        muRw_tt = q*mu_r1+p*mu_r2
        sigRw = q**2*sig11+p**2*sig22+2*p*q*sig12
        Rw_v = Rw.flatten(order="C")
        Zv2 = np.zeros(N*N)
        Zv2[ids] = -(muRw_tt[difv[ids]]-Rw_v[ids])/np.sqrt(sigRw[difv[ids]])
        
        if statistic in ["all", "weighted", "wei", "max" "m"]:
            Zmax = np.amax(Zv2[ids2])
            tauhat0 = np.where(Zv2 == Zmax)[0]
            tauhat = np.zeros((tauhat0.size, 2), dtype=np.int_)
            for i in np.arange(tauhat0.size):
                tauhat[i, 0] = np.int_(np.floor(tauhat0[i]/N))
                tauhat[i, 1] = np.int_(np.ceil(tauhat0[i]-1)%N+1)
            # tauhat = np.array([np.floor(tauhat0/N), np.ceil(tauhat0-1)%N+1], dtype="int64")
            weighted = {"tauhat" : tauhat, "Zmax" : Zmax, "Zw" : Zv2.reshape((N, -1)), "Rw" : Rw_v}
            scanZ["weighted"] = weighted
            
        if statistic in ["all", "generalized", "gen", "g", "max", "m"]:
            Rsub = R1-R2
            Rsub_v = Rsub.flatten(order="C")
            mu1_tt=mu_r1-mu_r2
            sig1 = sig11+sig22-2*sig12
            Zv1 = np.zeros(N*N)
            Zv1[ids] = -(mu1_tt[difv[ids]]-Rsub_v[ids])/np.sqrt(sig1[difv[ids]])
            
            if statistic in ["all", "max", "m"]:
                M = np.zeros(N*N)
                M[ids] = np.amax(np.stack((np.abs(Zv1[ids]), Zv2[ids]), axis=1), axis=1)
                Zmax = np.amax(M[ids2])
                tauhat0 = np.where(M == Zmax)[0]
                tauhat = np.zeros((tauhat0.size, 2), dtype=np.int_)
                for i in np.arange(tauhat0.size):
                    tauhat[i, 0] = np.int_(np.floor(tauhat0[i]/N))
                    tauhat[i, 1] = np.int_(np.ceil(tauhat0[i]-1)%N+1)
                # tauhat = np.array([np.floor(tauhat0/N), np.ceil(tauhat0-1)%N+1], dtype="int64")
                max_type = {"tauhat" : tauhat, "Zmax" : Zmax, "M" : M.reshape((N, -1))}
                scanZ["max_type"] = max_type
                
            if statistic in ["all", "generalized", "gen", "g"]:
                Zv = np.zeros(N*N)
                Zv[ids] = (Zv1[ids])**2+(Zv2[ids])**2
                Zmax = np.amax(Zv[ids2])
                tauhat0 = np.where(Zv == Zmax)[0]
                tauhat = np.zeros((tauhat0.size, 2), dtype=np.int_)
                for i in np.arange(tauhat0.size):
                    tauhat[i, 0] = np.int_(np.floor(tauhat0[i]/N))
                    tauhat[i, 1] = np.int_(np.ceil(tauhat0[i]-1)%N+1)
                # tauhat = np.array([np.floor(tauhat0/N), np.ceil(tauhat0-1)%N+1], dtype="int64")
                generalized = {"tauhat" : tauhat, "Zmax" : Zmax, "S" : Zv.reshape((N, -1))}
                scanZ["generalized"] = generalized
    
    return scanZ

# PVAL2
#               N:   the total number of nodes
#               E:   the edge matrix for the similarity graph
# connectivity[i]:   the list of nodes that are connected to i by an edge
#           scanZ:
#       statistic:   the scan statistics to be computed - a string indicating the type of scan statistic desired
#                    the default is "all"
#                    "all"                 - specifies all of the scan statistics (original, weighted, generalized, max-type)
#                    "o" or "original"     - specifies the original edge-count scan statistic
#                    "w" or "weighted"     - specifies the weighted edge-count scan statistic
#                    "g" or "generalized"  - specifies the generalized edge-count scan statistic
#                    "m" or "max"          - specifies the max-type edge-count scan statistic
#       skew_corr:   if True, the p-value approximation will incorporate skewness correction
#           lower:
#           upper:
def pval2(E, N, connectivity, scanZ, statistic="all", skew_corr=True, lower=None, upper=None):
    lower = np.int64(np.ceil(.05*N)) if lower is None else lower
    upper = np.int64(np.floor(.95*N)) if upper is None else upper
    output = {} # define an empty container to store the results
    edge_list = np.stack(np.nonzero(np.tril(E, k=-1))[::-1], axis=1) # get the edge list
    degrees = np.array([len(node) for node in connectivity]) # get the degree of each node
    sum_degrees_squared = np.sum(degrees**2) # calculate the sum of the squared degrees
    n_edges = np.int64(np.sum(degrees)/2) # calculate the number of edges in the similarity graph
    if skew_corr == False:
        if statistic in ["all", "original", "ori", "o"]:
            b = scanZ["original"]["Zmax"]
            if b > 0:
                def integrand_O(s):
                    x = rho1(N, s, n_edges, sum_degrees_squared)
                    return (b**2*x*Nu(np.sqrt(2*b**2*x)))**2*(N-s)
                pval_original = norm.pdf(b)/b*integrate.quad(integrand_O, a=lower, b=upper, limit=3000, epsabs=0.0001220703, epsrel=0.0001220703)[0]
            else:
                pval_original = 1
            output["original"] = np.amin(np.concatenate(([pval_original], [1])))
        if statistic in ["all", "weighted", "wei", "w"]:
            b = scanZ["weighted"]["Zmax"]
            if b > 0:
                def integrand_W(t):
                    x = rho1_Rw(N, t)
                    return (b**2*x*Nu(np.sqrt(2*b**2*x)))**2*(N-t)
                pval_weighted = norm.pdf(b)/b*integrate.quad(integrand_W, a=lower, b=upper, limit=3000, epsabs=0.0001220703, epsrel=0.0001220703)[0]
            else:
                pval_weighted = 1
            output["weighted"] = np.amin(np.concatenate(([pval_weighted], [1])))
        if statistic in ["all", "max", "m"]:
            b = scanZ["max_type"]["Zmax"]
            if b > 0:
                def integrand1(t):
                    x1 = N/(2*t*(N-t))
                    return (b**2*x1*Nu(np.sqrt(2*b**2*x1)))**2*(N-t)
                def integrand2(t):
                    x2 = rho1_Rw(N, t)
                    return (b**2*x2*Nu(np.sqrt(2*b**2*x2)))**2*(N-t)
                pval_u1 = 2*norm.pdf(b)/b*integrate.quad(integrand1, a=lower, b=upper, limit=3000, epsabs=0.0001220703, epsrel=0.0001220703)[0]
                pval_u2 = norm.pdf(b)/b*integrate.quad(integrand2, a=lower, b=upper, limit=3000, epsabs=0.0001220703, epsrel=0.0001220703)[0]
                pval_maxtype = 1-(1-np.amin(np.concatenate(([pval_u1], [1]))))*(1-np.amin(np.concatenate(([pval_u2], [1]))))
            else:
                pval_maxtype = 1
            output["max_type"] = pval_maxtype
        if statistic in ["all", "generalized", "gen", "g"]:
            b = scanZ["generalized"]["Zmax"]
            if b > 0:
                def integrand_G(t, w):
                    x1 = N/(2*t*(N-t))
                    x2 = rho1_Rw(N, t)
                    return (N-t)*(2*(x1*np.cos(w)**2+x2*np.sin(w)**2)*b*Nu(np.sqrt(2*b*(x1*np.cos(w)**2+x2*np.sin(w)**2))))**2/(2*np.pi)
                pval_generalized = chi2.pdf(b, 2)*integrate.dblquad(integrand_G, a=0, b=2*np.pi, gfun=lower, hfun=upper)[0]
            else:
                pval_generalized = 1
            output["generalized"] = np.amin(np.concatenate(([pval_generalized], [1])))
        return ouput
    x1 = np.sum(degrees*(degrees-1))
    x2 = np.sum(degrees*(degrees-1)*(degrees-2))
    x3 = 0
    for i in np.arange(edge_list.shape[0]):
        x3 = x3+(degrees[edge_list[i, 0]]-1)*(degrees[edge_list[i, 1]]-1)
    x4 = np.sum(degrees*(degrees-1)*(n_edges-degrees))
    x5 = 0
    for i in np.arange(edge_list.shape[0]):
        j = edge_list[i, 0]
        k = edge_list[i, 1]
        x5 = x5+np.sum(np.isin(connectivity[j], connectivity[k]))
    if statistic in ["all", "original", "ori", "o"]:
        b = scanZ["original"]["Zmax"]
        if b > 0:
            s = np.arange(1, N+1)
            x = rho1(N, s, n_edges, sum_degrees_squared)
            p1 = 2*s*(N-s)/(N*(N-1))
            p2 = 4*s*(s-1)*(N-s)*(N-s-1)/(N*(N-1)*(N-2)*(N-3))
            p3 = s*(N-s)*((N-s-1)*(N-s-2)+(s-1)*(s-2))/(N*(N-1)*(N-2)*(N-3))
            p4 = 8*s*(s-1)*(s-2)*(N-s)*(N-s-1)*(N-s-2)/(N*(N-1)*(N-2)*(N-3)*(N-4)*(N-5))
            mu = p1*n_edges
            sig = np.sqrt(p2*n_edges+(p1/2-p2)*sum_degrees_squared+(p2-p1**2)*n_edges**2)
            ER3 = p1*n_edges+p1/2*3*x1+p2*(3*n_edges*(n_edges-1)-3*x1)+p3*x2+p2/2*(3*x4-6*x3)+\
                  p4*(n_edges*(n_edges-1)*(n_edges-2)-x2-3*x4+6*x3)-2*p4*x5
            r = np.float64((mu**3+3*mu*sig**2-ER3))/np.float64(sig**3)
            theta_b = np.zeros(N)
            pos = np.where((1+(2*r*b)) > 0)[0]
            theta_b[pos] = (np.sqrt((1+(2*r*b))[pos])-1)/r[pos]
            ratio = np.exp((b-theta_b)**2/2+r*theta_b**3/6)/np.sqrt(1+r*theta_b)
            a = (b**2*x*Nu(np.sqrt(2*b**2*x)))**2*ratio
            nn = N-pos.size-1
            if nn > .75*N:
                def integrand(s):
                    x = rho1(N, s, n_edges, sum_degrees_squared)
                    return (b**2*x*Nu(np.sqrt(2*b**2*x)))**2*(N-s)
                pval_original = norm.pdf(b)/b*integrate.quad(integrand, a=lower, b=upper, limit=3000, epsabs=0.0001220703, epsrel=0.0001220703)[0]
                output["original"] = np.amin(np.concatenate(([pval_original], [1])))
            else:
                if nn >= (2*lower-1):
                    neg = np.where((1+(2*r*b)) <= 0)[0]
                    dif = neg[np.arange(1, nn)]-neg[np.arange(nn-1)]
                    id1 = np.argmax(dif)
                    id2 = id1+np.int64(np.ceil(.03*N))
                    id3 = id2+np.int64(np.ceil(.09*N))
                    inc = (a[id3]-a[id2])/(id3-id2)
                    a[np.arange(id2+1)[::-1]] = a[id2+1]-inc*np.arange(1, id2+2)
                    a[np.arange(np.int64(np.ceil(N/2)), N)] = a[np.arange(np.int64(N/2))[::-1]]
                    a[a < 0] = 0
                pval_original = norm.pdf(b)/b*integrate.quad(lambda s, arr=a, N=N: arr[np.int64(s)]*(N-s), a=lower, b=upper, limit=3000, epsabs=0.0001220703, epsrel=0.0001220703)[0]
                if not np.isnan(pval_original):
                    output["original"]=np.amin(np.concatenate(([pval_original], [1])))
                else:
                    def integrand(s):
                        x = rho1(N, s, n_edges, sum_degrees_squared)
                        return (b**2*x*Nu(np.sqrt(2*b**2*x)))**2*(N-s)
                    pval_original = norm.pdf(b)/b*integrate.quad(integrand, a=lower, b=upper, limit=3000, epsabs=0.0001220703, epsrel=0.0001220703)[0]
                    output["original"]=np.amin(np.concatenate(([pval_original], [1])))
        else:
            output["original"]=1
    if statistic in ["all", "weighted", "wei", "w", "max", "m"]:
        t = np.arange(1, N, dtype="float")
        A1 = n_edges*t*(t-1)/(N*(N-1))+3*x1*t*(t-1)*(t-2)/(N*(N-1)*(N-2))+\
             (3*n_edges*(n_edges-1)-3*x1)*t*(t-1)*(t-2)*(t-3)/(N*(N-1)*(N-2)*(N-3))+\
             x2*t*(t-1)*(t-2)*(t-3)/(N*(N-1)*(N-2)*(N-3))+(6*x3-6*x5)*(t*(t-1)*(t-2)*(t-3))/(N*(N-1)*(N-2)*(N-3))+\
             2*x5*(t*(t-1)*(t-2))/(N*(N-1)*(N-2))+(3*x4+6*x5-12*x3)*t*(t-1)*(t-2)*(t-3)*(t-4)/(N*(N-1)*(N-2)*(N-3)*(N-4))+\
             (n_edges*(n_edges-1)*(n_edges-2)+6*x3-2*x5-x2-3*x4)*t*(t-1)*(t-2)*(t-3)*(t-4)*(t-5)/(N*(N-1)*(N-2)*(N-3)*(N-4)*(N-5))
        B1 = (n_edges*(n_edges-1)-x1)*(t*(t-1)*(N-t)*(N-t-1))/(N*(N-1)*(N-2)*(N-3))+\
             (x4+2*x5-4*x3)*(t*(t-1)*(t-2)*(N-t)*(N-t-1))/(N*(N-1)*(N-2)*(N-3)*(N-4))+\
             (n_edges*(n_edges-1)*(n_edges-2)+\
             6*x3-2*x5-x2-3*x4)*t*(t-1)*(t-2)*(t-3)*(N-t)*(N-t-1)/(N*(N-1)*(N-2)*(N-3)*(N-4)*(N-5))
        C1 = (n_edges*(n_edges-1)-x1)*(N-t)*(N-t-1)*t*(t-1)/(N*(N-1)*(N-2)*(N-3))+\
             (x4+2*x5-4*x3)*(N-t)*(N-t-1)*(N-t-2)*t*(t-1)/(N*(N-1)*(N-2)*(N-3)*(N-4))+\
             (n_edges*(n_edges-1)*(n_edges-2)+\
             6*x3-2*x5-x2-3*x4)*t*(t-1)*(N-t)*(N-t-1)*(N-t-2)*(N-t-3)/(N*(N-1)*(N-2)*(N-3)*(N-4)*(N-5))
        D1 = n_edges*(N-t)*(N-t-1)/(N*(N-1))+3*x1*(N-t)*(N-t-1)*(N-t-2)/(N*(N-1)*(N-2))+\
             (3*n_edges*(n_edges-1)-3*x1)*(N-t)*(N-t-1)*(N-t-2)*(N-t-3)/(N*(N-1)*(N-2)*(N-3))+\
             x2*(N-t)*(N-t-1)*(N-t-2)*(N-t-3)/(N*(N-1)*(N-2)*(N-3))+\
             (6*x3-6*x5)*((N-t)*(N-t-1)*(N-t-2)*(N-t-3))/(N*(N-1)*(N-2)*(N-3))+\
             2*x5*((N-t)*(N-t-1)*(N-t-2))/(N*(N-1)*(N-2))+\
             (3*x4+6*x5-12*x3)*(N-t)*(N-t-1)*(N-t-2)*(N-t-3)*(N-t-4)/(N*(N-1)*(N-2)*(N-3)*(N-4))+\
             (n_edges*(n_edges-1)*(n_edges-2)+\
             6*x3-2*x5-x2-3*x4)*(N-t)*(N-t-1)*(N-t-2)*(N-t-3)*(N-t-4)*(N-t-5)/(N*(N-1)*(N-2)*(N-3)*(N-4)*(N-5))
        r1 = n_edges*(t*(t-1)/(N*(N-1)))+2*(0.5*sum_degrees_squared-n_edges)*t*(t-1)*(t-2)/(N*(N-1)*(N-2))+\
             (n_edges*(n_edges-1)-(2*(0.5*sum_degrees_squared-n_edges)))*t*(t-1)*(t-2)*(t-3)/(N*(N-1)*(N-2)*(N-3))
        r2 = n_edges*((N-t)*(N-t-1)/(N*(N-1)))+2*(0.5*sum_degrees_squared-n_edges)*(N-t)*(N-t-1)*(N-t-2)/(N*(N-1)*(N-2))+\
             (n_edges*(n_edges-1)-(2*(0.5*sum_degrees_squared-n_edges)))*(N-t)*(N-t-1)*(N-t-2)*(N-t-3)/(N*(N-1)*(N-2)*(N-3))
        r12 = (n_edges*(n_edges-1)-(2*(0.5*sum_degrees_squared-n_edges)))*t*(t-1)*(N-t)*(N-t-1)/(N*(N-1)*(N-2)*(N-3))
        x = rho1_Rw(N, t)
        q = (N-t-1)/(N-2)
        p = (t-1)/(N-2)
        mu = n_edges*(q*t*(t-1)+p*(N-t)*(N-t-1))/(N*(N-1))
        sig1 = q**2*r1+2*q*p*r12+p**2*r2-mu**2
        sig = np.sqrt(sig1)
        ER3 = q**3*A1+3*q**2*p*B1+3*q*p**2*C1+p**3*D1
        r = np.float64((ER3-3*mu*sig**2-mu**3))/np.float64(sig**3)
        r_Rw = r
        x_Rw = x
        if statistic in ["all", "weighted", "wei", "w"]:
            b = scanZ["weighted"]["Zmax"]
            result_u2 = pval2_sub2(N, b, r, x, lower, upper)
            if result_u2 > 0:
                output["weighted"] = np.amin(np.concatenate(([result_u2], [1])))
            else:
                if b > 0:
                    def integrand_W(t):
                        x = rho1_Rw(N, t)
                        return (b**2*x*Nu(np.sqrt(2*b**2*x)))**2*(N-t)
                    pval_weighted = norm.pdf(b)/b*integrate.quad(integrand_W, lower, upper, limit=3000, epsabs=0.0001220703, epsrel=0.0001220703)[0]
                else:
                    pval_weighted = 1
                output["weighted"] = np.amin(np.concatenate(([pval_weighted], [1])))
        if statistic in ["all", "max", "m"]:
            b = scanZ["max_type"]["Zmax"]
            x = N/(2*t*(N-t))
            q = 1
            p = -1
            mu = n_edges*(q*t*(t-1)+p*(N-t)*(N-t-1))/(N*(N-1))
            sig1 = q**2*r1+2*q*p*r12+p**2*r2-mu**2
            sig = np.sqrt(np.amax(np.stack((sig1, np.zeros(N-1)), axis=1), axis=1))
            ER3 = q**3*A1+3*q**2*p*B1+3*q*p**2*C1+p**3*D1
            r = np.float64((ER3-3*mu*sig**2-mu**3))/np.float64(sig**3)
            result_u1 = pval2_sub1(N, b, r, x, lower, upper)
            result_u2 = pval2_sub2(N, b, r_Rw, x_Rw, lower, upper)
            if (not result_u1 > 0) or (not result_u2 > 0):
                if b > 0:
                    def integrand1(t):
                        x1 = N/(2*t*(N-t))
                        return (b**2*x1*Nu(np.sqrt(2*b**2*x1)))**2*(N-t)
                    def integrand2(t):
                        x2 = rho1_Rw(N, t)
                        return (b**2*x2*Nu(np.sqrt(2*b**2*x2)))**2*(N-t)
                    pval_u1 = 2*norm.pdf(b)/b*integrate.quad(integrand1, lower, upper, limit=3000, epsabs=0.0001220703, epsrel=0.0001220703)[0]
                    pval_u2 = norm.pdf(b)/b*integrate.quad(integrand2, lower, upper, limit=3000, epsabs=0.0001220703, epsrel=0.0001220703)[0]
                    pval_maxtype = 1-(1-np.amin(np.concatenate(([pval_u1], [1]))))*(1-np.amin(np.concatenate(([pval_u2], [1]))))
                else:
                    pval_maxtype = 1
                output["max_type"] = pval_maxtype
            else:
                output["max_type"] = 1-(1-np.amin(np.concatenate(([result_u1], [1]))))*(1-np.amin(np.concatenate(([result_u2], [1]))))
    if statistic in ["all", "generalized", "gen", "g"]:
        b = scanZ["generalized"]["Zmax"]
        if b > 0:
            def integrand_G(t, w):
                x1 = N/(2*t*(N-t))
                x2 = rho1_Rw(N, t)
                return (N-t)*(2*(x1*np.cos(w)**2+x2*np.sin(w)**2)*b*Nu(np.sqrt(2*b*(x1*np.cos(w)**2+x2*np.sin(w)**2))))**2/(2*np.pi)
            pval_generalized = chi2.pdf(b, 2)*integrate.dblquad(integrand_G, a=0, b=2*np.pi, gfun=lower, hfun=upper)[0]
        else:
            pval_generalized = 1
        output["generalized"] = np.amin(np.concatenate(([pval_generalized], [1])))
    return output

# PVAL2_SUB1
#               N:   the total number of nodes
#               b:   Zmax
#               r:
#               x:
#           lower:
#           upper:
def pval2_sub1(N, b, r, x, lower, upper):
    if b < 0: return 1
    theta_b = np.zeros(N-1)
    pos = np.where((1+(2*r*b)) > 0)[0]
    theta_b[pos] = (np.sqrt((1+(2*r*b))[pos])-1)/r[pos]
    theta_b = np.nan_to_num(theta_b)
    ratio = np.exp((b-theta_b)**2/2 + r*theta_b**3/6)/np.sqrt(1+r*theta_b)
    a = (b**2*x*Nu(np.sqrt(2*b**2*x)))**2*ratio
    nn_l = np.int64(np.ceil(N/2))-(np.where(1+2*r[np.arange(np.int64(np.ceil(N/2)))]*b>0)[0]).size
    nn_r = np.int64(np.ceil(N/2))-(np.where(1+2*r[np.arange(np.int64(np.ceil(N/2)), (N-1))]*b>0)[0]).size
    if (nn_l > .35*N) or (nn_r > .35*N): return 0
    neg = np.where(1+2*r[np.arange(np.int64(np.ceil(N/2)))]*b<=0)[0]
    if nn_l >= lower:
        dif = np.concatenate((np.diff(neg), N/2-nn_l))
        id1 = np.argmax(dif)
        id2 = id1+np.int64(np.ceil(.03*N))
        id3 = id2+np.int64(np.ceil(.09*N))
        inc = (a[id3]-a[id2])/(id3-id2)
        a[np.arange(id2)[::-1]] = a[id2+1]-inc*(np.arange(id2))
    neg = np.where(1+2*r[np.arange(np.int64(np.ceil(N/2)), N+1)]*b<=0)[0]
    if nn_r >= (N-upper):
        id1 = np.amin(np.concatenate((neg+np.int64(np.ceil(N/2))-2, [np.int64(np.ceil(N/2))-2])))
        id2 = id1-np.int64(np.ceil(.03*N))
        id3 = id2-np.int64(np.ceil(.09*N))
        inc = (ratio[id3]-ratio[id2])/(id3-id2)
        ratio[np.arange(id2, (N-1))] = ratio[id2-1]+inc*((np.arange(id2, (N-1)))-id2)
        ratio[ratio < 0] = 0
        a = (b**2*x*Nu(np.sqrt(2*b**2*x)))**2*ratio
    a[a < 0] = 0
    return 2*norm.pdf(b)/b*integrate.quad(lambda s, arr=a, N=N: arr[np.int64(s)]*(N-s), a=lower, b=upper, limit=3000, epsabs=0.0001220703, epsrel=0.0001220703)[0]

# PVAL2_SUB2
#               N:   the total number of nodes
#               b:   Zmax
#               r:
#               x:
#           lower:
#           upper:
def pval2_sub2(N, b, r, x, lower, upper):
    if b < 0: return 1
    theta_b = np.zeros(N-1)
    pos = np.where((1+(2*r*b)) > 0)[0]
    theta_b[pos] = (np.sqrt((1+(2*r*b))[pos])-1)/r[pos]
    ratio = np.exp((b-theta_b)**2/2+r*theta_b**3/6)/np.sqrt(1+r*theta_b)
    a = (b**2*x*Nu(np.sqrt(2*b**2*x)))**2*ratio
    a = np.nan_to_num(a)
    nn = N-1-pos.size
    if nn > .75*N: return 0
    neg = np.where((1+(2*r*b))<=0)[0]
    if nn >= ((lower-1)+(N-upper)):
        dif = neg[1:nn]-neg[:(nn-1)]
        id1 = np.argmax(dif)
        id2 = id1+np.int64(np.ceil(.03*N))
        id3 = id2+np.int64(np.ceil(.09*N))
        inc = (a[id3]-a[id2])/(id3-id2)
        a[np.arange(id2)[::-1]] = a[id2+1]-inc*np.arange(id2)
        a[np.arange((np.int64(N/2)+1), N)] = a[np.arange(np.int64(N/2))[::-1]]
        a = np.nan_to_num(a)
        a[a < 0] = 0
    return norm.pdf(b)/b*integrate.quad(lambda s, arr=a, N=N: arr[np.int64(s)]*(N-s), a=lower, b=upper, limit=3000, epsabs=0.0001220703, epsrel=0.0001220703)[0]

# PERMPVAL2
def permpval2(N, connectivity, scanZ, statistic="all", B=100, n0=None, n1=None):
    n0 = np.int64(np.ceil(.05*N)) if n0 is None else np.int64(np.ceil(n0))
    n1 = np.int64(np.floor(.95*N)) if n1 is None else np.int64(np.floor(n1))
    original_Z = np.zeros(B)
    weighted_Z = np.zeros(B)
    max_type_Z = np.zeros(B)
    generalized_Z = np.zeros(B)
    index = np.arange(N, dtype="int64")
    # index = np.array([1, 6, 9, 4, 3, 2, 8, 7, 5, 0])
    for b in np.arange(B):
        # shuffle the index vector
        np.random.shuffle(index)
        # reverse the index and value of the shuffled index vector (permutation)
        # this tells us the order in which to grab from the connectivity list according to the shuffle (permutation)
        permmatch = np.zeros(N, dtype="int64")
        for i in np.arange(N):
            permmatch[index[i]] = i
        connectivity_star = []
        for i in np.arange(N):
            oldlinks = connectivity[permmatch[i]]
            connectivity_star.append(index[oldlinks])
        changepoint_star = changepoint2(connectivity_star, N, statistic, n0, n1)
        if statistic in ["all", "original", "ori", "o"]:
            original_Z[b] = changepoint_star["original"]["Zmax"]
        if statistic in ["all", "weighted", "wei", "w"]:
            weighted_Z[b] = changepoint_star["weighted"]["Zmax"]
        if statistic in ["all", "max", "m"]:
            max_type_Z[b] = changepoint_star["max_type"]["Zmax"]
        if statistic in ["all", "generalized", "gen", "g"]:
            generalized_Z[b] = changepoint_star["generalized"]["Zmax"]
    output = {}
    p = 1-(np.arange(B))/B
    if statistic in ["all", "original", "ori", "o"]:
        maxZ = np.amax(original_Z)
        maxZs = np.sort(original_Z)
        output["original"] = {"pval" : np.average(original_Z >= scanZ["original"]["Zmax"]),
                              "curve" : np.concatenate((maxZs.reshape((-1, 1)), p.reshape((-1, 1))), axis=1), "maxZ" : maxZ, "Z" : original_Z}
    if statistic in ["all", "weighted", "wei", "w"]:
        maxZ = np.amax(weighted_Z)
        maxZs = np.sort(weighted_Z)
        output["weighted"] = {"pval" : np.average(weighted_Z >= scanZ["weighted"]["Zmax"]),
                              "curve" : np.concatenate((maxZs.reshape((-1, 1)), p.reshape((-1, 1))), axis=1), "maxZ" : maxZ, "Z" : weighted_Z}
    if statistic in ["all", "max", "m"]:
        maxZ = np.amax(max_type_Z)
        maxZs = np.sort(max_type_Z)
        output["max_type"] = {"pval" : np.average(max_type_Z >= scanZ["max_type"]["Zmax"]),
                              "curve" : np.concatenate((maxZs.reshape((-1, 1)), p.reshape((-1, 1))), axis=1), "maxZ" : maxZ, "Z" : max_type_Z}
    if statistic in ["all", "generalized", "gen", "g"]:
        maxZ = np.amax(generalized_Z)
        maxZs = np.sort(generalized_Z)
        output["generalized"] = {"pval" : np.average(generalized_Z >= scanZ["generalized"]["Zmax"]),
                                 "curve" : np.concatenate((maxZs.reshape((-1, 1)), p.reshape((-1, 1))), axis=1), "maxZ" : maxZ, "Z" : generalized_Z}
    return output

# GSEG2
#          N:   the number of observations (nodes in the sequence)
#          E:   the edge matrix for the similarity graph
#  statistic:   the scan statistics to be computed - a string indicating the type of scan statistic desired
#               the default is "all"
#               "all"                 - specifies all of the scan statistics (original, weighted, generalized, max-type)
#               "o" or "original"     - specifies the original edge-count scan statistic
#               "w" or "weighted"     - specifies the weighted edge-count scan statistic
#               "g" or "generalized"  - specifies the generalized edge-count scan statistic
#               "m" or "max"          - specifies the max-type edge-count scan statistic
#         n0:   the minimum length of the interval to be considered as a change interval
#         n1:   the maximum length of the interval to be considered as a change interval
#  pval_appr:   if True, the function returns the p-value approximation(s) based on asymptotic properties
#  skew_corr:   (only when pval_asym=True) if True, the p-value approximation will incorporate skewness correction
#  pval_perm:   if True, the function returns p-values from doing B permutations
#          B:   (only when pval.perm=True) the number of iterations to run with permutation
def gseg2(E, N, statistic="all", n0=None, n1=None, pval_asym=True, skew_corr=True, pval_perm=False, B=100):
    # define default values for n0 and n1, which are functions of N
    if n0 is None:
        n0 = np.int64(np.ceil(.05*N))
    elif n0 < 2:
        n0 = np.int64(2)
    else:
        n0 = np.int64(np.ceil(n0))
    
    if n1 is None:
        n1 = np.int64(np.floor(.95*N))
    elif n1 > (N-2):
        n1 = np.int64(N-2)
    else:
        n1 = np.int64(np.floor(n1))
    
    # create a storage container for the results
    r1 = {}
    
    # create a connectivity list
    # that is, connectivity[i] is the numpy array of nodes that are connected to node i by an edge
    connectivity = []
    for i in np.arange(N):
        connectivity.append(np.nonzero(E[i])[0])
    
    r1["scanZ"] = changepoint2(connectivity = connectivity, N=N, statistic=statistic, n0=n0, n1=n1)
    
    # get the p-values
    if pval_asym == True:
        r1["pval_asym"] = pval2(E=E, N=N, connectivity=connectivity, scanZ=r1["scanZ"],
                                statistic=statistic, skew_corr=skew_corr, lower=n0, upper=n1)
    if pval_perm == True:
        r1["pval_perm"] = permpval2(N=N, connectivity=connectivity, scanZ=r1["scanZ"],
                                   statistic=statistic, B=B, n0=n0, n1=n1)
    return r1