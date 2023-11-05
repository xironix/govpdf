import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def save_data(df, file_path):
    df.to_csv(file_path, index=False)

def move_applied_entries(jobs_df, applied_df, index):
    applied_entry = jobs_df.loc[index]
    jobs_df = jobs_df.drop(index)
    applied_df = applied_df.append(applied_entry, ignore_index=True)
    return jobs_df, applied_df
