import pandas as pd
import random

def delete_random_data(df, deletion_rate=0.1):
    dirty_df = df.copy()
    for column in dirty_df.columns:
        if dirty_df[column].dtype == "object":
            for idx, _ in dirty_df.iterrows():
                if random.random() < deletion_rate:
                    dirty_df.at[idx, column] = None
        else:
            for idx, _ in dirty_df.iterrows():
                if random.random() < deletion_rate:
                    dirty_df.at[idx, column] = float('nan')
    return dirty_df
