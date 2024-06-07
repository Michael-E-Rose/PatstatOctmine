import pandas as pd
import toml


def main():
    # Load the paths from the config file
    config = toml.load('config.toml')
    paths = config['paths']

    # Read the data files
    octimine = pd.read_feather(paths['octimine_file'])
    patent_no = pd.read_csv(paths['patent_no'])

    # Select only the required columns from patent_no
    patent_no_selected = patent_no[['docdb_family_id', 'earliest_pat_publn_id', 'earliest_filing_date']].copy()
    patent_no_selected['earliest_filing_year'] = pd.to_datetime(patent_no_selected['earliest_filing_date']).dt.year
    patent_no_selected.drop(columns=['earliest_filing_date'], inplace=True)

    # Merge octimine with patent_no on docdb_family_id1 and docdb_family_id2
    merged = (octimine
              .merge(patent_no_selected, how='left', left_on='docdb_family_id1',
                     right_on='docdb_family_id', suffixes=('', '_docdb1'))
              .merge(patent_no_selected, how='left', left_on='docdb_family_id2',
                     right_on='docdb_family_id', suffixes=('', '_docdb2'))
              .drop(columns=['docdb_family_id', 'docdb_family_id1', 'docdb_family_id2', "docdb_family_id_docdb2"])
              )

    merged.rename(columns={
        'earliest_pat_publn_id': 'patent_no1',
        'earliest_filing_year': 'earliest_filing_year1',
        'earliest_pat_publn_id_docdb2': 'patent_no2',
        'earliest_filing_year_docdb2': 'earliest_filing_year2'
    }, inplace=True)

    # Save Snippet as a CSV file
    merged.head(100).to_csv(paths['snippet_csv'], index=False)

    # Save the final DataFrame as a Feather file
    merged.to_feather(paths['output_feather'])


if __name__ == '__main__':
    main()
