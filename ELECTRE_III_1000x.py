import time
from pyDecision.algorithm import electre_iii
from download_dataset import *

# COMPLETE THE DATA
step = 0.01
criteria_count = 2
# Q_list = [0, 0.05, 0.1, 0.15, 0.2, 0.4]
# P_list = [round(q + 0.05,2) for q in Q_list]
# V_list = [1 - q for q in Q_list]
W_list = [1]  # weights
MIDDLE_POINT = np.array([0.5 for i in range(0, criteria_count)])
####################
Q_list = [0.1]
P_list = [0.2]
V_list = [0.8]

dataset = download_dataset_with_middle_point(step, criteria_count)


def create_electre_III_dataset(Q_val, P_val, V_val, W_val, dataset=dataset):
    # Initiate variables
    Q = np.full((1, criteria_count), Q_val)[0]
    P = np.full((1, criteria_count), P_val)[0]
    V = np.full((1, criteria_count), V_val)[0]
    W = np.full((1, criteria_count), W_val)[0]

    global_concordance, credibility, rank_D, rank_A, rank_N, rank_P = electre_iii(dataset, P = P, Q = Q, V = V, W = W, graph = False)
    p1 = rank_P

    # translate the result to numbers(so they can correspond in visualisation with colors)
    # middle point < point -> 3 "-"
    # middle point > point -> 1 "P+"
    # middle point = point -> 2 (within the indistinguishability threshold) "I"
    # incomparable -> 0 "R"
    final_scores_matrix = np.array([])
    for i in range(0, len(p1)-1):
        print(p1[-1][i])
        if p1[-1][i] == 'P+':
            final_scores_matrix = np.append(final_scores_matrix, 1)
        elif p1[-1][i] == 'I':
            final_scores_matrix = np.append(final_scores_matrix, 2)
        elif p1[-1][i] == 'P-':
            final_scores_matrix = np.append(final_scores_matrix, 3)
        elif p1[-1][i] == 'R':
            final_scores_matrix = np.append(final_scores_matrix, 0)
        elif p1[-1][i] == '-':
            final_scores_matrix = np.append(final_scores_matrix, np.nan)
        print(final_scores_matrix)
        final_scores_matrix = final_scores_matrix.reshape(-1, 1)

    df = join_scores_matrix_and_dataset(final_scores_matrix, dataset[:-1, :])

    save_data_to_file(df, f"data/ELECTRE_III_1000x/ELE_III_1000x_Q{Q_val}_P{P_val}_V{V_val}_W{W_val}.csv")


full_time = 0
counter = 0
for Q in Q_list:
    for P in P_list:
        for V in V_list:
            for W in W_list:
                start_time = time.perf_counter()
                create_electre_III_dataset(Q_val=Q, P_val=P, V_val=V, W_val=W)
                counter += 1
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                full_time += elapsed_time
                print(f"Elapsed time: {elapsed_time} seconds")


average_time = full_time/counter
print(f"Average time: {average_time} seconds")