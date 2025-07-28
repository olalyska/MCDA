import numpy as np
from numpy import genfromtxt
from download_dataset import download_dataset
from download_dataset import save_data_to_file
from download_dataset import *

# COMPLETE THE DATA
step = 0.01
criteria_count = 2
threshold = 0.02
W_val = 1  # Weights Value
criterion_type_val = 'max'  # Criterion Type: 'max' or 'min'
MIDDLE_POINT = np.array([[0.5 for i in range(0, criteria_count)]], dtype=float)
####################


# Download set of points
dataset = download_dataset(step, criteria_count)


def create_topsis_dataset(dataset=dataset, threshold=threshold, W_val=W_val, criterion_type_val=criterion_type_val):
    weights = np.full((1, criteria_count), W_val)[0]
    criterion_type = np.full((1, criteria_count), criterion_type_val)[0]
    X = np.copy(dataset)
    w = np.copy(weights)

    # Normalization - minmax
    min_val = np.min(X, axis=0)
    max_val = np.max(X, axis=0)
    range_val = np.where(max_val - min_val == 0, 1, max_val - min_val)
    r_ij = (X - min_val) / range_val

    # # Normalization - vector
    # sum_cols = np.sum(X*X, axis = 0)
    # sum_cols = sum_cols**(1/2)
    #
    # r_ij = X/sum_cols

    v_ij = r_ij * w
    p_ideal_A = np.zeros(X.shape[1])
    n_ideal_A = np.zeros(X.shape[1])
    for i in range(0, dataset.shape[1]):
        if (criterion_type[i] == 'max'):
            p_ideal_A[i] = np.max(v_ij[:, i])
            n_ideal_A[i] = np.min(v_ij[:, i])
        else:
            p_ideal_A[i] = np.min(v_ij[:, i])
            n_ideal_A[i] = np.max(v_ij[:, i])
    p_s_ij = (v_ij - p_ideal_A) ** 2
    p_s_ij = np.sum(p_s_ij, axis=1) ** (1 / 2)
    n_s_ij = (v_ij - n_ideal_A) ** 2
    n_s_ij = np.sum(n_s_ij, axis=1) ** (1 / 2)
    closeness_matrix = n_s_ij / (p_s_ij + n_s_ij)

# translate the result to numbers(so they can correspond in visualisation with colors)
    # point > middle point -> 3 "-"
    # point < middle point -> 1 "P+"
    # point = middle point -> 2 (within the indistinguishability threshold) "I"
    # incomparable -> 0 "R"
    middle_point_closeness = closeness_matrix[-1]
    final_scores_matrix = np.array([])
    for i in range(0, len(closeness_matrix)):
        point_closeness = closeness_matrix[i]
        if abs(middle_point_closeness - point_closeness) < threshold:
            final_scores_matrix = np.append(final_scores_matrix, 2)
            np.append(dataset[i], 2)
        elif point_closeness > middle_point_closeness:
            final_scores_matrix = np.append(final_scores_matrix, 3)
        elif point_closeness < middle_point_closeness:
            final_scores_matrix = np.append(final_scores_matrix, 1)
        else:
            print("error")
        final_scores_matrix = final_scores_matrix.reshape(-1, 1)

    df = join_scores_matrix_and_dataset(final_scores_matrix, dataset)

    save_data_to_file(df, f"data/TOPSIS_MINMAX/TOP_MINMAX_TH{threshold}_W{W_val}.csv")


threshold_list = [0.1, 0.02, 0.2]

for threshold in threshold_list:
    create_topsis_dataset(dataset, threshold)