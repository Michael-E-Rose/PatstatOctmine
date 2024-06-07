import pandas as pd
import toml


def main():
    # Load the paths from the config file
    config = toml.load('config.toml')
    paths = config['paths']

    # Read the feather file
    df = pd.read_feather(paths['octimine_file'])

    # Get unique entries from 'docdb_family_id1' and 'docdb_family_id2'
    unique_entries = set(df['docdb_family_id1']).union(df['docdb_family_id2'])

    # Create a DataFrame from the unique entries
    unique_df = pd.DataFrame(unique_entries, columns=['unique_family_ids'])

    # Save the unique entries to a CSV file
    unique_df.to_csv(paths['unique_family_ids'], index=False)


if __name__ == '__main__':
    main()
