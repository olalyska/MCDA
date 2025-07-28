import numpy as np
from numpy import genfromtxt
import pandas as pd
from pyDecision.algorithm import electre_iii
from download_dataset import *

# COMPLETE THE DATA
step = 0.02
criteria_count = 2
Q_val = 0.3
P_val = 0.5
V_val = 0.7
W_val = 0.5
MIDDLE_POINT = np.array([[0.5 for i in range(0, criteria_count)]], dtype=float)
####################

dataset = download_dataset(step, criteria_count)

def create_electre_III_dataset(Q_val=Q_val, P_val=P_val, V_val=V_val, W_val=W_val, dataset=dataset):
    # Initiate variables
    Q = np.full((1, criteria_count), Q_val)[0]
    P = np.full((1, criteria_count), P_val)[0]
    V = np.full((1, criteria_count), V_val)[0]
    W = np.full((1, criteria_count), W_val)[0]

    global_concordance, credibility, rank_D, rank_A, rank_N, rank_P = electre_iii(dataset, P = P, Q = Q, V = V, W = W, graph = False)
    p1 = rank_P

    # translate the result to numbers(so they can correspond in visualisation with colors)
    # point > middle point -> 3 "-"
    # point < middle point -> 1 "P+"
    # point = middle point -> 2 (within the indistinguishability threshold) "I"
    # incomparable -> 0 "R"
    final_scores_matrix = np.array([])
    for i in range(0, len(p1)):
        if p1[-1][i] == 'P+':
            final_scores_matrix = np.append(final_scores_matrix, 1)
        elif p1[-1][i] == 'I':
            final_scores_matrix = np.append(final_scores_matrix, 2)
        elif p1[-1][i] == 'P-':
            final_scores_matrix = np.append(final_scores_matrix, 3)
        elif p1[-1][i] == 'R':
            final_scores_matrix = np.append(final_scores_matrix, 0)
        elif p1[-1][i] == '-':
            final_scores_matrix = np.append(final_scores_matrix, 0)
        final_scores_matrix = final_scores_matrix.reshape(-1, 1)

    df = join_scores_matrix_and_dataset(final_scores_matrix, dataset)
    # final_scores_matrix = final_scores_matrix.astype(np.int64)
    # points_plus_final_scores = np.hstack((dataset, final_scores_matrix))
    # points_plus_final_scores = points_plus_final_scores.astype(object)
    # points_plus_final_scores[:, -1] = points_plus_final_scores[:, -1].astype(int)
    # df = pd.DataFrame(points_plus_final_scores)

    # save the data to file
    save_data_to_file(df, f"data/ELECTRE_III/ELE_III_Q{Q_val}_P{P_val}_V{V_val}_W{W_val}.csv")


Q_list = [0.1]
# S_list = [0, 0.2, 0.4, 0.6, 0.8, 1]
P_list = [0.2]
# P_list = [0, 0.2, 0.4, 0.6, 0.8, 1]
V_list = [0.8]
W_list = [1]



for Q in Q_list:
    for P in P_list:
        for V in V_list:
            for W in W_list:
                create_electre_III_dataset(Q_val=Q, P_val=P, V_val=V, W_val=W)