from numpy import genfromtxt
import numpy as np
import pandas as pd

def download_dataset(step, criteria_count, M_val=0.5):
    MIDDLE_POINT = np.array([[M_val for i in range(0, criteria_count)]], dtype=float)
    try:
        data = genfromtxt(f'data/datasets/dataset_s{step}_c{criteria_count}.csv', delimiter=',')
    except:
        print(
            f"Generate data via generete_points.py script with step = {step} and criteria_count = {criteria_count}")
        exit(1)
    dataset = np.concatenate((data, MIDDLE_POINT), axis=0)
    return dataset

download_dataset(0.02, 2)
def join_scores_matrix_and_dataset(final_scores_matrix, dataset):
    final_scores_matrix = final_scores_matrix.astype(np.int64)
    points_plus_final_scores = np.hstack((dataset, final_scores_matrix))
    points_plus_final_scores = points_plus_final_scores.astype(object)
    points_plus_final_scores[:, -1] = points_plus_final_scores[:, -1].astype(int)
    df = pd.DataFrame(points_plus_final_scores[:-1])
    return df


def save_data_to_file(df, filename):
    df.to_csv(filename, index=False, header=False)
    print(f"Dataset: {filename} created")


