from data import load_data, save_data, move_applied_entries
from populate import populate_pdf_form


def main():
    jobs_df = load_data('jobs.csv')
    applied_df = load_data('applied.csv')

    # Assume that the jobs_df DataFrame is iterated over and PDFs are populated
    for index, row in jobs_df.iterrows():
        pdf_path = populate_pdf_form('path/to/pdf/template', row)
        jobs_df, applied_df = move_applied_entries(jobs_df, applied_df, index)

        # Save after each iteration or after all iterations depending on the requirement
        save_data(jobs_df, 'jobs.csv')
        save_data(applied_df, 'applied.csv')

        print(f"PDF form populated and saved to {pdf_path}")


if __name__ == "__main__":
    main()
