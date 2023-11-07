import pandas as pd


def get_result_mapping():
    results_mapping = {
        'Networking': {'New Contacts Added': 0.8, 'Follow-up Meeting Arranged': 0.2},
        'Interview': {'Second Round': 0.3, 'Offer Received': 0.1, 'No Offer': 0.6},
        'Resume Review': {'Feedback Received': 0.7, 'Updated Resume': 0.3},
        'Cover Letter Drafting': {'Draft Completed': 0.5, 'Sent with Application': 0.5},
        'Job Application': {'Applied': 0.8, 'Position Filled': 0.2},
        'LinkedIn Profile Update': {'Profile Updated': 0.7, 'New Connections Made': 0.3},
    }
    return results_mapping


def get_activity_types():
    activity_type_weights = {
        'Networking': 0.10,
        'Interview': 0.05,
        'Resume Review': 0.05,
        'Cover Letter Drafting': 0.05,
        'Job Application': 0.70,
        'LinkedIn Profile Update': 0.05,
    }

    return activity_type_weights


def print_activities(activity_type_weights):
    # Print all activity types
    print("Activity Types:")
    for activity_type in activity_type_weights:
        print(activity_type)


def load_data(file_path):
    return pd.read_csv(file_path)


def save_data(df, file_path):
    df.to_csv(file_path, index=False)


def move_applied_entries(jobs_df, applied_df, index):
    applied_entry = jobs_df.loc[index]
    jobs_df = jobs_df.drop(index)
    applied_df = applied_df.append(applied_entry, ignore_index=True)
    return jobs_df, applied_df

