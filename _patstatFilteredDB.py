import pandas as pd
from tqdm import tqdm


def main():
    path = r'/home/pery@ip.local/f-newton/PATSTAT/2023-10/DTA/tls201.dta'
    unique_ids = pd.read_csv('doc_db_unique_family_ids.csv')

    # Convert the unique_family_ids column to a set for faster lookup
    unique_ids_set = set(unique_ids['unique_family_ids'])

    reader = pd.read_stata(path, chunksize=100000)

    # Initialize a flag to write header only once
    header_written = False

    # Iterate over each chunk with tqdm to show the progress bar
    for chunk in tqdm(reader, desc="Reading chunks"):
        # Filter the chunk
        filtered_chunk = chunk[chunk['docdb_family_id'].isin(unique_ids_set)]

        # Append the filtered chunk to the CSV file
        filtered_chunk.to_csv('filtered_patstat_db.csv', mode='a', header=not header_written, index=False)

        # After first write, set header_written to True
        if not header_written:
            header_written = True

    print("Filtered data saved to 'filtered_test_file.csv'")


if __name__ == '__main__':
    main()
