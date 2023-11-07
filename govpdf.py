from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime, timedelta
import random
import data

# Function to generate a list of random dates within the last two weeks
def generate_random_dates(num_random_dates):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=14)
    random_dates = [(start_date + timedelta(
        seconds=random.uniform(0, (end_date - start_date).total_seconds()))).strftime('%Y %b %d') for _ in range(num_random_dates)]
    return random_dates


def select_activity_type_by_weight(activity_type_weights):
    total_weight = sum(activity_type_weights.values())
    random_num = random.uniform(0, total_weight)
    cumulative_weight = 0
    for activity_type, weight in activity_type_weights.items():
        cumulative_weight += weight
        if random_num <= cumulative_weight:
            return activity_type
    return None

def generate_random_result(activity_type, results_mapping):
    possible_results = results_mapping[activity_type]
    total_weight = sum(possible_results.values())
    random_num = random.uniform(0, total_weight)
    cumulative_weight = 0
    for result, weight in possible_results.items():
        cumulative_weight += weight
        if random_num <= cumulative_weight:
            return result
    return None


def populate_pdf_form(pdf_template_path, jobs_df, num_rows_to_fill, resume_prep):
    # Extract the possible results and their weights for the given activity type
    pdf_reader = PdfReader(pdf_template_path)
    pdf_writer = PdfWriter()
    output_pdf_path = 'HR0077_populated.pdf'


    for i, page in enumerate(pdf_reader.pages):
        pdf_writer.add_page(page)

        for j in range(num_rows_to_fill):
            sorted_dates = sorted(generate_random_dates(num_rows_to_fill))
            selected_activity_type = select_activity_type_by_weight(data.get_activity_types())
            selected_result = generate_random_result(selected_activity_type, data.get_result_mapping())

            # It appears you want to use selected_activity_type here, not activity_type
            print(f"Processing activity type: {selected_activity_type}")

            field_values = {
                f'DATERow{j + 1}': sorted_dates[j],
                f'TYPERow{j + 1}': selected_activity_type,
                f'RESULTSRow{j + 1}': selected_result,
                f'LOCATIONRow{j + 1}': 'Home',
                f'CONTACTRow{j + 1}': 'N/A'
            }

            if selected_activity_type == 'Job Application':
                field_values[f'CONTACTRow{j + 1}'] = jobs_df.at[j, 'CONTACT']
                field_values[f'LOCATIONRow{j + 1}'] = jobs_df.at[j, 'COMPANY']
            elif selected_activity_type == 'Interview':
                field_values[f'LOCATIONRow{j + 1}'] = jobs_df.at[j, 'COMPANY'] + ' ' + jobs_df.at[j, 'LOCATION']

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

