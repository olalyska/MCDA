import numpy as np
from pyDecision.algorithm import topsis_method
from numpy import genfromtxt
from download_dataset import *


# COMPLETE THE DATA
step = 0.01
criteria_count = 2
threshold = 0.02
W_val = 0.5  # Weights Value
criterion_type_val = 'max' # Criterion Type: 'max' or 'min'
MIDDLE_POINT = np.array([[0.5 for i in range(0, criteria_count)]], dtype=float)
####################


# Download set of points
dataset = download_dataset(step, criteria_count)

def create_topsis_dataset(threshold = threshold, dataset=dataset, W_val = W_val, criterion_type_val=criterion_type_val):
    weights = np.full((1, criteria_count), W_val)[0]
    criterion_type = np.full((1, criteria_count), criterion_type_val)[0]
    closeness_matrix = topsis_method(dataset, weights, criterion_type, graph=False, verbose=False)
    middle_point_closeness = closeness_matrix[-1]

    # translate the result to numbers(so they can correspond in visualisation with colors)
    # point > middle point -> 3 "-"
    # point < middle point -> 1 "P+"
    # point = middle point -> 2 (within the indistinguishability threshold) "I"
    # incomparable -> 0 "R"
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
    save_data_to_file(df=df, filename=f"data/TOPSIS_US/TOP_US_TH{threshold}_W{W_val}.csv")


threshold_list = [0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

for threshold in threshold_list:
    create_topsis_dataset(threshold, dataset)
