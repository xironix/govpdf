import pandas as pd
import random
from datetime import datetime, timedelta
from PyPDF2 import PdfReader, PdfWriter
import data

# Read the CSV file into a DataFrame
jobs_df = pd.read_csv('jobs.csv')
output_pdf_path = 'HR0077_populated.pdf'
pdf_template_path = "HR0077.pdf"

# Define the maximum number of rows you have in your PDF
min_rows = 20
max_rows = 30  # Adjust to the actual number of rows in your PDF

# Choose a random number of rows to fill out
num_rows_to_fill = random.randint(1, max_rows)

# Variable to determine if the resume prep row should be included
resume_prep = True

# Function to generate a list of random dates within the last two weeks
def generate_random_dates(num_random_dates):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=14)
    random_dates = [start_date + timedelta(
        seconds=random.uniform(0, (end_date - start_date).total_seconds())) for _ in range(num_random_dates)]
    return random_dates


def generate_random_result(activity_type, results_mapping):
    if activity_type in results_mapping:
        return random.choice(results_mapping[activity_type])
    else:
        return random.choice(result_mapping["Job Application"])

    return None

# Function to populate the PDF form
def populate_pdf_form(pdf_template_path, output_pdf_path, jobs_df, results_mapping, num_rows_to_fill, resume_prep,
                      min_rows, max_rows):
    applied_indices = []
    sorted_dates = sorted(generate_random_dates(num_rows_to_fill))
    pdf_reader = PdfReader(pdf_template_path)
    pdf_writer = PdfWriter()

    for i, page in enumerate(pdf_reader.pages):
        pdf_writer.add_page(page)

        for j in range(num_rows_to_fill):
            sorted_dates = sorted(generate_random_dates(num_rows_to_fill))
            result_for_row = generate_random_result(random.choice(list(results_mapping.keys())), results_mapping)

            field_values = {
                f'DATERow{j + 1}': sorted_dates[j],
                f'TYPERow{j + 1}': result_for_row,
                f'RESULTSRow{j + 1}': result_for_row,
                f'LOCATIONRow{j + 1}': 'Home' if result_for_row == 'LinkedIn Profile Update' else f"{jobs_df.at[j, 'COMPANY']} {jobs_df.at[j, 'LOCATION']}",
                f'CONTACTRow{j + 1}': 'N/A'
            }

            if j == 0 and resume_prep:
                field_values.update({
                    f'DATERow{j + 1}': 'Working on resume',
                    f'TYPERow{j + 1}': 'Resume Review',
                    f'LOCATIONRow{j + 1}': 'Home',
                    f'RESULTSRow{j + 1}': 'Updated',
                    f'CONTACTRow{j + 1}': 'N/A'
                })

            pdf_writer.update_page_form_field_values(pdf_writer.pages[i], field_values)

    with open(output_pdf_path, "wb") as output_pdf_file:
        pdf_writer.write(output_pdf_file)

    return output_pdf_path, applied_indices

# Main function
if __name__ == '__main__':
    # Define file paths
    jobs_csv_path = 'jobs.csv'
    applied_csv_path = 'applied_jobs.csv'  # Assuming you have an applied jobs CSV file
    output_pdf_path = 'HR0077_populated.pdf'
    pdf_template_path = "HR0077.pdf"
    resume_prep = True

    # Define the range for the number of rows in the PDF
    min_rows = 20
    max_rows = 30

    # Dictionary mapping activity types to results
    results_mapping = {
        'Networking': ['New Contacts Added', 'Follow-up Meeting Arranged'],
        'Interview': ['Second Round', 'Offer Received', 'No Offer'],
        'Job Application': ['Application Acknowledged', 'Interview Invitation', 'No Response'],
        'Skill Development': ['Module Completed', 'Certification Achieved'],
        'Career Workshop': ['Attended', 'Missed'],
        'Resume Review': ['Feedback Received', 'Updated Resume'],
        'Cover Letter Drafting': ['Draft Completed', 'Sent with Application'],
        'Recruitment Call': ['Scheduled Interview', 'Information Received'],
        'Online Course': ['Course Started', 'Course Completed'],
        'Career Counseling': ['Session Attended', 'Action Plan Created'],
        'LinkedIn Profile Update': ['Profile Updated', 'New Connections Made'],
        'Informational Interview': ['Insights Gained', 'Referral Obtained']
    }

    # Get a list of all activity types
    activity_types = list(results_mapping.keys())

    # Print all activity types
    print("Activity Types:")
    for activity_type in activity_types:
        print(activity_type)

    # Instead of reading the CSV directly, use the load_data function from data.py
    jobs_df = data.load_data(jobs_csv_path)
    # If you have an applied jobs dataframe, load it as well
    # applied_df = data.load_data(applied_csv_path)

    # Determine the number of rows to populate in the PDF
    num_rows_to_fill = random.randint(min_rows, max_rows)

    # Populate the PDF form
    populated_pdf_path = populate_pdf_form(pdf_template_path, output_pdf_path, jobs_df, results_mapping, num_rows_to_fill, resume_prep, min_rows, max_rows)
    print(f"PDF form populated and saved to {populated_pdf_path}")

    # Move the applied jobs from jobs_df to applied_df
    #for index in applied_job_indices:
    #    jobs_df, applied_df = data.move_applied_entries(jobs_df, applied_df, index)

    # Save the updated jobs and applied jobs dataframes
    #data.save_data(jobs_df, jobs_csv_path)
    #data.save_data(applied_df, applied_csv_path)
