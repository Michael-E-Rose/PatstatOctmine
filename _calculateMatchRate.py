import pandas as pd

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    unique_ids = pd.read_csv('doc_db_unique_family_ids.csv')
    patstat_ids = pd.read_csv('filtered_patstat_db.csv')

    unique_ids_set = set(unique_ids['unique_family_ids'])
    unique_patstat_id_set = set(patstat_ids['docdb_family_id'])

    matched_ids = unique_ids_set.intersection(unique_patstat_id_set)
    match_rate = len(matched_ids) / len(unique_ids_set) * 100

    print(f"Total unique IDs: {len(unique_ids_set)}")
    print(f"Matched IDs: {len(matched_ids)}")
    print(f"Match rate: {match_rate:.2f}%")



