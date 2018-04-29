import csv
import pytest
from wrdbm.extractor import DBMExtractor

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


