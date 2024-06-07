import pandas as pd


def main():
    path = r'/home/pery@ip.local/f-newton/PATSTAT/2023-10/ep_ma5_all.ftr'
    octimine = pd.read_feather(path)
    patent_no = pd.read_csv("patstat_pat_no.csv")

    # Select only the required columns from patent_no
    patent_no_selected = patent_no[['docdb_family_id', 'earliest_pat_publn_id', 'earliest_filing_date']]

    # Convert 'earliest_filing_date' to datetime and extract year
    patent_no_selected['earliest_filing_year'] = pd.to_datetime(patent_no_selected['earliest_filing_date']).dt.year
    patent_no_selected = patent_no_selected.drop(columns=['earliest_filing_date'])

    # Merge octimine with patent_no on docdb_family_id1
    merged_df1 = octimine.merge(patent_no_selected, how='left', left_on='docdb_family_id1', right_on='docdb_family_id',
                                suffixes=('', '_docdb1'))

    # Merge the result with patent_no on docdb_family_id2
    merged_df2 = merged_df1.merge(patent_no_selected, how='left', left_on='docdb_family_id2',
                                  right_on='docdb_family_id', suffixes=('', '_docdb2'))

    # Drop the additional docdb_family_id columns to avoid confusion
    merged_df2 = merged_df2.drop(columns=['docdb_family_id', "docdb_family_id1",
                                          "docdb_family_id2", "docdb_family_id_docdb2"])

    # Renaming columns for clarity
    merged_df2.rename(columns={
        'earliest_pat_publn_id': 'patent_no1',
        'earliest_filing_year_docdb1': 'earliest_filing_year',
        'earliest_pat_publn_id_docdb2': 'patent_no2',
        'earliest_filing_year_docdb2': 'earliest_filing_year_2',
    }, inplace=True)

    # Save the final DataFrame as a Feather file
    # output_path = r'/home/pery@ip.local/f-newton/PATSTAT/2023-10/octimine_with_patent_no.ftr'
    # merged_df2.to_feather(output_path)


if __name__ == '__main__':
    main()
