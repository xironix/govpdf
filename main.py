import govpdf
import data
import random

# Main function
if __name__ == '__main__':

    # Variable to determine if the resume prep row should be included
    resume_prep = True
    # Define file paths
    jobs_csv_path = 'jobs.csv'
    applied_csv_path = 'applied_jobs.csv'  # Assuming you have an applied jobs CSV file
    pdf_template_path = "HR0077.pdf"
    resume_prep = True


    # Instead of reading the CSV directly, use the load_data function from data.py
    jobs_df = data.load_data(jobs_csv_path)
    # If you have an applied jobs dataframe, load it as well
    # applied_df = data.load_data(applied_csv_path)

    # Determine the number of rows to populate in the PDF
    num_rows_to_fill = random.randint(15, 30)

    # Populate the PDF form
    populated_pdf_path = govpdf.populate_pdf_form(pdf_template_path, jobs_df, num_rows_to_fill, resume_prep)
    print(f"PDF form populated and saved to {populated_pdf_path}")
