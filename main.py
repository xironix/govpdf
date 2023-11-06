import pandas as pd
import random
from datetime import datetime, timedelta
from PyPDF2 import PdfReader, PdfWriter

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


def generate_random_result(activity_types, results_mapping):
    results = {}
    for activity_type in activity_types:
        if activity_type not in results_mapping:
            raise ValueError(f"Activity type '{activity_type}' is not in the results mapping.")
        results[activity_type] = random.choice(results_mapping[activity_type])
    return results

# Function to populate the PDF form
def populate_pdf_form(pdf_template_path, output_pdf_path, jobs_df, results_mapping, num_rows_to_fill, resume_prep,
                      min_rows, max_rows):
    sorted_dates = sorted(generate_random_dates(num_rows_to_fill))
    pdf_reader = PdfReader(pdf_template_path)
    pdf_writer = PdfWriter()

    for i, page in enumerate(pdf_reader.pages):
        pdf_writer.add_page(page)
        for j in range(num_rows_to_fill):
            sorted_dates = sorted(generate_random_dates(num_rows_to_fill))
            activity_type = jobs_df.loc[j, 'ActivityType']

            if activity_type not in results_mapping:
                raise ValueError(f"Activity type '{activity_type}' is not a valid type in the results mapping.")

            result_for_row = generate_random_result(activity_type, results_mapping)

            field_values = {
                f'DATERow{j + 1}': generate_random_dates(num_rows_to_fill),
                f'TYPERow{j + 1}': result_for_row,
                f'RESULTSRow{j + 1}': generate_random_result(result_for_row, results_mapping),
                f'LOCATIONRow{j + 1}': 'Home' if result_for_row == 'LinkedIn Profile Update' else f"{jobs_df.at[j, 'COMPANY']} {jobs_df.at[j, 'LOCATION']}",
                f'CONTACTRow{j + 1}': 'N/A'
            }

            if activity_type in contact_required_types and not (j == 0 and resume_prep):
                field_values[f'CONTACTRow{j + 1}'] = jobs_df.at[j, 'CONTACT']

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

    return output_pdf_path


# Main function
#if __name__ == '__main__':
    # Define file paths
    jobs_csv_path = 'jobs.csv'
    output_pdf_path = 'HR0077_populated.pdf'
    pdf_template_path = "HR0077.pdf"

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
        'Portfolio Update': ['Portfolio Enhanced', 'New Projects Added'],
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

    random_result = generate_random_result(activity_types, results_mapping)

    # Read jobs data
    jobs_df = pd.read_csv(jobs_csv_path)

    # Determine the number of rows to populate in the PDF
    num_rows_to_fill = random.randint(min_rows, max_rows)

    # Decide whether resume preparation is required
    resume_prep = True  # Replace with your logic

    # Populate the PDF form
    populated_pdf_path = populate_pdf_form(pdf_template_path, output_pdf_path, jobs_df, results_mapping, num_rows_to_fill, resume_prep, min_rows, max_rows)
    print(f"PDF form populated and saved to {populated_pdf_path}")