import pandas as pd
from tqdm import tqdm
import toml


def main():
    # Load the paths from the config file
    config = toml.load('config.toml')
    paths = config['paths']

    # Read the unique IDs file
    unique_ids = pd.read_csv(paths['unique_family_ids'])

    # Convert the unique_family_ids column to a set for faster lookup
    unique_ids_set = set(unique_ids['unique_family_ids'])

    # Read the Patstat file in chunks
    reader = pd.read_stata(paths['tls201_file'], chunksize=100000)

    # Initialize a flag to write header only once
    header_written = False

    # Iterate over each chunk with tqdm to show the progress bar
    for chunk in tqdm(reader, desc="Reading chunks"):
        # Filter the chunk
        filtered_chunk = chunk[chunk['docdb_family_id'].isin(unique_ids_set)]

        # Append the filtered chunk to the CSV file
        filtered_chunk.to_csv(paths['patstat_filtered'], mode='a', header=not header_written, index=False)

        # After first write, set header_written to True
        if not header_written:
            header_written = True


if __name__ == '__main__':
    main()
