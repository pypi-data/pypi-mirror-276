import click
import csv
import sqlite_utils
from .utils import convert_csv_to_sqlite

@click.command()
@click.argument(
    "export_file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
def cli(export_file, db_path):
    "Convert exported CSV from Visible app to a SQLite DB"
    db = sqlite_utils.Database(db_path)

    with open(export_file, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)

        convert_csv_to_sqlite(csvreader, db)
