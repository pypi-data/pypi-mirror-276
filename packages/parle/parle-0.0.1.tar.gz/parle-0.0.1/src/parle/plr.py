from revolutionhtl.nxTree import is_leaf
from networkx import dfs_postorder_nodes
from itertools import chain, combinations, product
import pandas as pd
from revolutionhtl.lca_rmq import LCA
import numpy as np


def plr_disimilarity(T_i, T_j, mu_i, mu_j, Ts, S_matrix= None, alpha= None, diameter= None, labelAttr= 'label', eventAttr= 'event'):
    S_matrix, alpha= _check_aux(Ts, S_matrix, alpha, labelAttr)
    diameter= _compute_diamter(T_i, Ts, alpha, diameter)
    d_ij= _plr_asymmetric(T_i, T_j, mu_i, mu_j, S_matrix, alpha, labelAttr, eventAttr)
    d_ji= _plr_asymmetric(T_j, T_i, mu_j, mu_i, S_matrix, alpha, labelAttr, eventAttr)
    return (d_ij+d_ji)/diameter

def _compute_S_matrix(S, labelAttr):
    M= _init_S_matrix(S, labelAttr)
    descendants= dict()
    for x_node in dfs_postorder_nodes(S, S.root):
        x_label= S.nodes[x_node][labelAttr]
        if is_leaf(S, x_node):
            # Track descendants
            descendants[x_label]= {x_label}
        else:
            Y= set((S.nodes[y][labelAttr] for y in S[x_node]))
            # Distance from x to descendants: P_xz= P_yz + 1
            for y_label in Y:
                for z_label in descendants[y_label]:
                    M.loc[x_label,z_label]= M.loc[y_label,z_label] + 1
                    M.loc[z_label,x_label]= M.loc[x_label,z_label]
            # Distance between two descendants z and z1: P_zz1= P_xz + P_xz1
            for y_label,y1_label in combinations(Y, 2):
                for z_label,z1_label in product(descendants[y_label], descendants[y1_label]):
                    M.loc[z_label, z1_label]= M.loc[x_label,z_label] + M.loc[x_label,z1_label]
                    M.loc[z1_label, z_label]= M.loc[z_label, z1_label]
            # Track descendants
            descendants[x_label]= set(chain.from_iterable((descendants[y_label]
                                                          for y_label in Y))) .union( {x_label} )
    return M.loc

def _plr_asymmetric(T_i, T_j, mu_i, mu_j, S_matrix, alpha, labelAttr, eventAttr):
    E_ij= _compute_equivalent_nodes(T_i, T_j, labelAttr)
    d_path= lambda x: S_matrix[mu_i[T_i.nodes[x][labelAttr]], mu_j[T_j.nodes[E_ij[x]][labelAttr]]]
    d_lbl= lambda x: T_i.nodes[x][eventAttr] != T_j.nodes[E_ij[x]][eventAttr]
    d_ij= lambda x: alpha*d_path(x) + (1-alpha)*d_lbl(x)
    return sum(map(d_ij, dfs_postorder_nodes(T_i, source= T_i.root)))

def _compute_equivalent_nodes(T_i, T_j, labelAttr):
    E_ij= _init_E_ij(T_i, T_j, labelAttr)
    induced_leafs= dict()
    for i_node in dfs_postorder_nodes(T_i):
        if is_leaf(T_i, i_node):
            # Add induced leaf
            induced_leafs[i_node]= { E_ij[ i_node ] }
        else:
            # compute induced leafs
            induced_leafs[i_node]= set(chain.from_iterable((induced_leafs[x] for x in T_i[i_node])))
            # compute LCA in T_j
            E_ij[i_node]= LCA(T_j, induced_leafs[i_node])
    return E_ij

def _check_aux(Ts, S_matrix, alpha, labelAttr):
    if S_matrix==None:
        S_matrix= _compute_S_matrix(Ts, labelAttr)
    if alpha==None:
        n_species= _count_leafs(Ts)
        alpha= 1/n_species
    return S_matrix, alpha

def _compute_diamter(T_i, Ts, alpha, diameter):
    if diameter==None:
        n= _count_leafs(Ts)
        m= _count_leafs(T_i)
        diameter= 2*alpha*(n-2)*(m-1) + 2*(1-alpha)*(m-1)
    return diameter

def _init_S_matrix(S, labelAttr):
    index= [S.nodes[x][labelAttr] for x in dfs_postorder_nodes(S, S.root)]
    N= len(index)
    return pd.DataFrame(np.zeros((N,N)), columns= index, index= index)

def _init_E_ij(T_i, T_j, labelAttr):
    # Check leafs
    i_leafs= _label_2_leaf(T_i, labelAttr)
    j_leafs= _label_2_leaf(T_j, labelAttr)
    if set(i_leafs) != set(j_leafs):
        raise ValueError('The leafs of the trees are not the same')
    # Init E_ij
    return {x : j_leafs[x_label] for x_label,x in i_leafs.items()}

_count_leafs= lambda T: sum((is_leaf(T, x) for x in T))
_label_2_leaf= lambda T, attr: {T.nodes[x][attr] : x for x in _leafs_iterator(T)}
_leafs_iterator= lambda T: (x for x in T if is_leaf(T, x))
