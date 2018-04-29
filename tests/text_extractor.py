from wrdbm.extractor import DBMExtractor
import csv
import os

CREDENTIALS = {
    'client_secret': os.getenv('WR_CLIENT_SECRET'),
    'client_id': os.getenv('WR_CLIENT_ID'),
    'refresh_token': os.getenv('WR_REFRESH_TOKEN')
}


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
