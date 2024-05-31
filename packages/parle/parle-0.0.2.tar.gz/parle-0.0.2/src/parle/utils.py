from .plr import plr_disimilarity, _check_aux, _compute_diamter
from .errors import NonUniqueNodeLabels

from revolutionhtl.nhxx_tools import read_nhxx

from pandas import DataFrame, read_csv
from itertools import combinations
from networkx import dfs_postorder_nodes

def compute_plr_dataframe_all_vs_all(df, Ts, treeCol= 'tree', muCol= 'mu', indexCol= None,
                                     S_matrix= None, alpha= None, labelAttr= 'label', eventAttr= 'event',
                                     diameter= None,
                                    ):
    _check_labels_all_vs_all(df, Ts, labelAttr, treeCol)

    S_matrix, alpha= _check_aux(Ts, S_matrix, alpha, labelAttr)
    diameter= _compute_diamter(df[treeCol].iloc[0], Ts, alpha, diameter)
    if indexCol!=None:
        df= df.set_index(indexCol)

    df_distances= []
    for i,j in combinations(df.index, 2):
        d_plr= plr_disimilarity(df.loc[i,treeCol], df.loc[j,treeCol],
                                df.loc[i,muCol], df.loc[j,muCol],
                                Ts, S_matrix, alpha, diameter,
                                labelAttr, eventAttr)
        df_distances+= [[f"{i}-vs-{j}", d_plr]]
    return DataFrame(df_distances, columns= ['trees', 'plr_disimilarity'])

def compute_plr_dataframe_rows(df, Ts, tree_i_Col= 'tree_i', tree_j_Col= 'tree_j',
                               mu_i_Col= 'mu_i', mu_j_Col= 'mu_j', S_matrix= None,
                               alpha= None, labelAttr= 'label', eventAttr= 'event',
                                     diameter= None,
                                    ):
    _check_labels_rows(df, Ts, labelAttr, tree_i_Col, tree_j_Col)

    S_matrix, alpha= _check_aux(Ts, S_matrix, alpha, labelAttr)
    diameter= _compute_diamter(df[tree_i_Col].iloc[0], Ts, alpha, diameter)
    d_plr= lambda row: plr_disimilarity(row[tree_i_Col], row[tree_j_Col],
                                        row[mu_i_Col], row[mu_j_Col],
                                        Ts, S_matrix, alpha, diameter,
                                        labelAttr, eventAttr)
    return df.apply(d_plr, axis= 1)

def check_label_uniqueness(T, labelAttr):
    nodes= list(dfs_postorder_nodes(T, T.root))
    labels= set((T.nodes[x][labelAttr] for x in nodes))
    return len(nodes)==len(labels)

def load_df_all_vs_all(path, treeCol= 'tree', muCol= 'mu'):
    df= read_csv(path, sep='\t')
    df[treeCol]= df[treeCol].apply(_set_roots)
    df[muCol]= df[muCol].apply(_txtMu_2_dict)
    return df

def load_df_rows(path, tree_i_Col= 'tree_i', tree_j_Col= 'tree_j', mu_i_Col= 'mu_i', mu_j_Col= 'mu_j'):
    df= read_csv(path, sep='\t')
    df[tree_i_Col]= df[tree_i_Col].apply(_set_roots)
    df[tree_j_Col]= df[tree_j_Col].apply(_set_roots)
    df[mu_i_Col]= df[mu_i_Col].apply(_txtMu_2_dict)
    df[mu_j_Col]= df[mu_j_Col].apply(_txtMu_2_dict)
    return df

def _set_roots(nhx):
    T= read_nhxx(nhx)
    T.root= 1
    T.planted_root= 0
    return T

def _txtMu_2_dict(txt):
    return dict(map(lambda x: x.split(':'), txt.split(',')))

txt_map= lambda X: ','.join((f"{a}:{b}" for a,b in X.items()))

def _check_labels_all_vs_all(df, Ts, labelAttr, treeCol):
    if not check_label_uniqueness(Ts, labelAttr):
        raise NonUniqueNodeLabels('Labels of species tree are not unique')
    if not df[treeCol].apply(lambda T: check_label_uniqueness(T, labelAttr)).all():
        raise NonUniqueNodeLabels('There are gene trees with non unique albels')

def _check_labels_rows(df, Ts, labelAttr, tree_i_Col, tree_j_Col):
    if not check_label_uniqueness(Ts, labelAttr):
        raise NonUniqueNodeLabels('Labels of species tree are not unique')
    if not df[tree_i_Col].apply(lambda T: check_label_uniqueness(T, labelAttr)).all():
        raise NonUniqueNodeLabels('There are gene trees with non unique albels')
    if not df[tree_j_Col].apply(lambda T: check_label_uniqueness(T, labelAttr)).all():
        raise NonUniqueNodeLabels('There are gene trees with non unique albels')
