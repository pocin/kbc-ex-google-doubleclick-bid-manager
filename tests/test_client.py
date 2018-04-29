import os
import pytest
from exdbm.extractor import DBMExtractor
import csv

CREDENTIALS = {
    'client_secret': os.getenv('WR_CLIENT_SECRET'),
    'client_id': os.getenv('WR_CLIENT_ID'),
    'refresh_token': os.getenv('WR_REFRESH_TOKEN')
}


def test_creating_authenticated_client_from_refresh_token():
    dbmc = DBMExtractor(**CREDENTIALS)
    assert isinstance(dbmc.access_token, str)

def test_downloading_lineitems(tmpdir):
    outpath = tmpdir.join('lineitems.csv')
    ex = DBMExtractor(**CREDENTIALS)
    outpath_ = ex.download_and_clean_lineitems(
        outpath.strpath,
        filter_type='LINE_ITEM_ID',
        filter_ids=[1576228])
    with open(outpath_) as out:
        first_line = next(csv.DictReader(out))
        assert first_line['Line Item Id'] == str(1576228)

def test_converting_lineitems_json_to_csv(tmpdir):

    infile = tmpdir.join("lineitems_input.json")
    infile.write(r'{"lineItems": "columnA,columnB\n\"value\",value2"}')
    outfile = tmpdir.join("outfile.csv")

    DBMExtractor._clean_lineitems_response_via_ijson(infile.strpath, outfile.strpath)

    with open(outfile.strpath) as inf:
        reader = csv.DictReader(inf)
        first_line = next(reader)
        assert first_line['columnA'] == 'value'
        assert first_line['columnB'] == 'value2'
        assert len(first_line.keys()) == 2
        with pytest.raises(StopIteration):
            next(reader)

