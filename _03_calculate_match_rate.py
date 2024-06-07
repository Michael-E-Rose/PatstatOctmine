import pandas as pd
import toml


def main():
    # Load the paths from the config file
    config = toml.load('config.toml')
    paths = config['paths']

    # Read the CSV files
    unique_ids = pd.read_csv(paths['unique_family_ids'])
    patstat_ids = pd.read_csv(paths['patstat_filtered'])

    # Convert the columns to sets for faster lookup
    unique_ids_set = set(unique_ids['unique_family_ids'])
    unique_patstat_id_set = set(patstat_ids['docdb_family_id'])

    # Find the intersection of the two sets
    matched_ids = unique_ids_set.intersection(unique_patstat_id_set)
    match_rate = len(matched_ids) / len(unique_ids_set) * 100

    # Print the results
    print(f"Total unique IDs: {len(unique_ids_set)}")
    print(f"Matched IDs: {len(matched_ids)}")
    print(f"Match rate: {match_rate:.2f}%")


if __name__ == '__main__':
    main()
