import numpy as np
import pandas as pd
import itertools

# ADJUST THE DATA HERE #
step = 0.02
criteria_count = 2
########################


def create_dataset(step, criteria_count, filename=f"data/dataset.csv"):
    values = np.arange(0, 1 + step, step)
    dataset = np.array(list(itertools.product(values, repeat=criteria_count)))
    df = pd.DataFrame(dataset)
    df = df.round(decimals=4)
    df.to_csv(filename, index=False, header=False)


create_dataset(step, criteria_count, filename=f"data/dataset_s{step}_c{criteria_count}.csv")

