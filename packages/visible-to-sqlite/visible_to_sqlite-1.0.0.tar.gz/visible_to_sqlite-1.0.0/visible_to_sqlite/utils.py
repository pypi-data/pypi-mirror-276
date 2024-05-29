import datetime

def convert_csv_to_sqlite(csvreader, db):
    csvreader.fieldnames[-1] = csvreader.fieldnames[-1].strip()
    for row in csvreader:
        save_observation(db, row)

def save_observation(db, row):
    db["Observations"].insert({
            "observation_date": row["observation_date"],
            "value": row["observation_value"],
            "tracker": db["Trackers"].lookup({
                "name":  row["tracker_name"]
            },
            {"tracker_category": row["tracker_category"]},
            extracts={"tracker_category": "TrackerCategories"}),
        },
        hash_id_columns=("observation_date", "tracker"),
        foreign_keys=[("tracker", "Trackers")],
        columns={"observation_date": datetime.date},
        replace=True)
