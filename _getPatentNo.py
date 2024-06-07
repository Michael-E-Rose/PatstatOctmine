import pandas as pd
from tqdm import tqdm


def process_filtered_database(filtered_database_file):
    # Load the filtered data
    df = pd.read_csv(filtered_database_file)

    # Ensure the earliest_filing_year column is in datetime format
    df['earliest_filing_date'] = pd.to_datetime(df['earliest_filing_date'])

    # List to store docdb_family_id with None entries
    none_entries = []

    # Define a function to get the prioritized entry for each group
    def get_earliest_filing_date_entry(group):
        docdb_family_id = group['docdb_family_id'].iloc[0]

        # Check for EP entries
        ep_entries = group[group['appln_auth'] == 'EP']
        if not ep_entries.empty:
            return ep_entries.loc[ep_entries['earliest_filing_date'].idxmin()]

        # Check for WO entries
        wo_entries = group[group['appln_auth'] == 'WO']
        if not wo_entries.empty:
            return wo_entries.loc[wo_entries['earliest_filing_date'].idxmin()]

        # Check for US entries that are granted
        us_entries = group[(group['appln_auth'] == 'US') & (group['granted'] == 'Y')]
        if not us_entries.empty:
            return us_entries.loc[us_entries['earliest_filing_date'].idxmin()]

        # If no entries match the criteria, save group and return None
        none_entries.append(docdb_family_id)
        return None

    tqdm.pandas(desc="Processing DocDB Family IDs")

    # Group by docdb_family_id and apply the prioritization function
    df_earliest_filing_date = (df.groupby('docdb_family_id', group_keys=False)
                               .progress_apply(get_earliest_filing_date_entry)
                               .reset_index(drop=True))

    # Drop any None entries that may have been returned by the function
    df_earliest_filing_date = df_earliest_filing_date.dropna()

    # Save the entries to a new CSV file
    header = ["docdb_family_id", "earliest_pat_publn_id", "earliest_filing_date", "appln_auth", "granted"]
    df_earliest_filing_date.to_csv('patstat_pat_no.csv', index=False, columns=header)

    # Print number of non-EP entries
    non_ep_entries_count = len(df_earliest_filing_date[df_earliest_filing_date['appln_auth'] != 'EP'])
    print(f"Non-EP entries: {non_ep_entries_count}")

    # Save the list of docdb_family_id with None entries to a log file
    with open('none_entries_log.txt', 'w') as f:
        for entry in none_entries:
            f.write(f"{entry}\n")

    print(f"Logged {len(none_entries)} None entries to 'none_entries_log.txt'")


def main():
    filtered_database_file = 'filtered_patstat_db.csv'
    process_filtered_database(filtered_database_file)


if __name__ == '__main__':
    main()
