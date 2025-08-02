import numpy as np
import pandas as pd
import itertools
import os

# ADJUST THE DATA HERE #
step = 0.5
criteria_count = 2  #number of criteria
########################


def create_dataset(step, criteria_count, filename):
    values = np.arange(0, 1 + step, step)
    dataset = np.array(list(itertools.product(values, repeat=criteria_count)))
    df = pd.DataFrame(dataset)
    df = df.round(decimals=4)
    if not os.path.exists(f"data"):
      os.makedirs('data')
      print("Directory created successfully!")
    else:
      print("Directory already exists!")
    df.to_csv(filename, index=False, header=False)


create_dataset(step, criteria_count, filename=f"data/datasets/dataset_s{step}_c{criteria_count}.csv")

