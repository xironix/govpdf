# ... (other functions needed for populating the PDF)

def populate_pdf_form(pdf_path, jobs_df, types_list, results_mapping, min_rows, max_rows, resume_prep):
    # Ensure the minimum is not greater than the maximum
    min_rows = min(min_rows, max_rows)
    # Choose a random number of rows to fill out, ensuring it's at least the minimum
    num_rows_to_fill = random.randint(min_rows, max_rows)

    # Generate a list of random dates for the number of rows to fill
    random_dates = [generate_random_date() for _ in range(num_rows_to_fill)]
    # Sort the list of dates
    sorted_dates = sorted(random_dates, key=lambda x: datetime.strptime(x, '%Y-%m-%d'))

    # Debug: Print the sorted dates to verify
    print("Sorted Dates:", sorted_dates)

    pdf_reader = PdfReader(pdf_path)
    pdf_writer = PdfWriter()

    for i, page in enumerate(pdf_reader.pages):
        pdf_writer.add_page(page)
        for j in range(num_rows_to_fill):
            # Use the sorted date for each row
            date_for_row = sorted_dates[j]

            # Generate a random type for the entry unless it's the first row and resume_prep is True
            activity_type = generate_random_type(types_list) if not (j == 0 and resume_prep) else 'Resume Review'

            # Initialize field values with default contact as 'N/A'
            field_values = {
                f'DATERow{j+1}': generate_random_date(),
                f'TYPERow{j+1}': activity_type,
                f'LOCATIONRow{j+1}': 'Home' if activity_type == 'LinkedIn Profile Update' else f"{jobs_df.at[j, 'COMPANY']} {jobs_df.at[j, 'LOCATION']}",
                f'RESULTSRow{j+1}': generate_random_result(activity_type, results_mapping),
                f'CONTACTRow{j+1}': 'N/A'  # Default to 'N/A'
            }

            # If the activity type requires a contact, update the contact field value
            if activity_type in contact_required_types and not (j == 0 and resume_prep):
                field_values[f'CONTACTRow{j+1}'] = jobs_df.at[j, 'CONTACT']

            # Special case for the first row if resume preparation is needed
            if j == 0 and resume_prep:
                field_values.update({
                    f'DATERow{j+1}': 'Working on resume',  # or use generate_random_date() if date is needed
                    f'TYPERow{j+1}': 'Resume Review',
                    f'LOCATIONRow{j+1}': 'Home',
                    f'RESULTSRow{j+1}': 'Updated',
                    f'CONTACTRow{j+1}': 'N/A'  # Assuming no contact is needed for resume prep
                })

            pdf_writer.update_page_form_field_values(pdf_writer.pages[i], field_values)

    # Save the populated PDF to a file
    with open(output_pdf_path, "wb") as output_pdf_file:
        pdf_writer.write(output_pdf_file)

    return output_pdf_path