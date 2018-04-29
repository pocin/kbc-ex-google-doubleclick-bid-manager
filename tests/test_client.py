import os
import pytest
from wrdbm.writer import DBMWriter
import csv

CREDENTIALS = {
    'client_secret': os.getenv('WR_CLIENT_SECRET'),
    'client_id': os.getenv('WR_CLIENT_ID'),
    'refresh_token': os.getenv('WR_REFRESH_TOKEN')
}


def test_creating_authenticated_client_from_refresh_token():
    dbmc = DBMWriter(**CREDENTIALS)
    assert isinstance(dbmc.access_token, str)


def test_writing_ok_response_to_csv(tmpdir):
    fake_response = {
        "uploadStatus": {
            "errors": None, #TODO: HOW DOES ERR RESP LOOK LIKE
            "rowStatus": [{
                "rowNumber": 1,
                "entityId": 12,
                "entityName": "string",
                "changed": True,
                "persisted": True,
                "errors": ["foo"]
            }]
        }
    }
    outpath = (tmpdir.mkdir('out')
                     .mkdir('files')
                     .join('line_items_status.csv'))

    real_outpath = DBMWriter.lineitems_response_to_csv(
        resp_json=fake_response,
        outpath=outpath.strpath)

    assert os.path.isfile(real_outpath)
    assert real_outpath == outpath.strpath
    header = fake_response['uploadStatus']['rowStatus'][0].keys()
    with open(real_outpath) as inf:
        reader = csv.DictReader(
            inf,)
            # fieldnames=header)

        first_row = next(reader)
        assert first_row['entityId'] == "12"
        with pytest.raises(StopIteration):
            next(reader)
