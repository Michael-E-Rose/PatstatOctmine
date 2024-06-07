import pandas as pd


def main():
    path = r'/home/pery@ip.local/f-newton/PATSTAT/2023-10/ep_ma5_all.ftr'

    df = pd.read_feather(path)

    unique_entries = set(df['docdb_family_id1']).union(df['docdb_family_id2'])

    unique_df = pd.DataFrame(unique_entries, columns=['unique_family_ids'])

    unique_df.to_csv('doc_db_unique_family_ids.csv', index=False)


if __name__ == '__main__':
    main()
