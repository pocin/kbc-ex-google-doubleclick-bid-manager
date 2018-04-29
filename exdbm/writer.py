"""
The writer
"""
from pathlib import Path
import csv
import logging
from wrdbm.client import DBMClient
import voluptuous as vp


def validate_params(params):
    schema = vp.Schema(
        {
            "write": {
                "lineItems": {
                    "dryRun": vp.Coerce(bool),
                    "filename": str
                }
            }
        }
    )
    return schema(params)

def main(datadir, credentials, params):
    params_cleaned = validate_params(params)
    config_lineitems = params_cleaned['lineItems']
    writer = DBMWriter(**credentials)
    path_lineitems_in = Path(datadir) / 'in/tables/' / config_lineitems['filename']
    path_lineitems_out = Path(datadir) / 'out/tables/' / 'line_items_status.csv'
    writer.process_lineitems(path_lineitems_in, path_lineitems_out, dry_run=config_lineitems['dryRun'])


class DBMWriter(DBMClient):
    def upload_lineitems(self, items, dry_run=True):
        payload = {'lineItems': items, 'dryRun': dry_run}
        return self.post('/lineitems/uploadlineitems', json=payload).json()

    @staticmethod
    def lineitems_response_to_csv(
            resp_json,
            outpath='/data/out/files/line_items_status.json'):
        logging.info("Serializing job status to csv")
        errors = resp_json['uploadStatus']['errors']
        if errors:
            raise ValueError("couldn't upload lineitems: %s", errors)
        try:
            first_row = resp_json['uploadStatus']['rowStatus'][0]
        except IndexError:
            logging.info("No rows in the input lineitems csv!")
            return None
        with open(outpath, 'w') as outf:
            writer = csv.DictWriter(outf, fieldnames=first_row.keys())
            writer.writeheader()
            writer.writerow(first_row)
            for row in resp_json['uploadStatus']['rowStatus'][1:]:
                writer.writerow(row)

        return outpath

    def process_lineitems(self, path_in, path_out, dry_run=True):
        """
        Read csv, make request, log response to csv

        """
        logging.info("Processing %s with dry_run=%s", path_in, dry_run)
        with open(path_in, 'r') as fin:
            csv_items = csv.reader(fin).read()
        resp = self.upload_lineitems(items=csv_items, dry_run=dry_run)

        logging.info("Serializing status to %s", path_out)
        true_outpath = DBMWriter.lineitems_response_to_csv(resp, path_out)
        return true_outpath
