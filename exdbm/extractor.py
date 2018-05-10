"""extractor
"""
from exdbm.client import DBMClient
import random
from pathlib import Path
import json
import ijson
import voluptuous as vp
import logging


class DBMExtractor(DBMClient):
    def _download_lineitems(self, outpath, filter_type, filter_ids=None):
        payload = {
            "filterType": filter_type,
        }
        if filter_ids:
            payload["filterIds"] = filter_ids

        with open(outpath, 'wb') as out:
            for chunk in self.post_stream("/lineitems/downloadlineitems", json=payload):
                out.write(chunk)
        return outpath

    @staticmethod
    def _clean_lineitems_response_via_ijson(inpath, outpath):
        with open(inpath) as f:
            # conntains just 1 lineitem but we still need to iterate
            for item in ijson.items(f, 'lineItems'):
                with open(outpath, 'w') as fout:
                    fout.write(item)
        return outpath

    @staticmethod
    def _clean_lineitems_response(inpath, outpath):
        """the input json looks like this
        '{"lineItems": "actual,csv\ncontents,yes"}'
        so this function skips the first and last json string

        DOESN'T WORK AT THE MOMENT as the csv is JSON escaped and we would need
        to unescape \n and "

        """
        raise NotImplementedError("Dont use this")
        offset_beginning = 17
        offset_tail = -4

        chunksize = 1024
        with open(inpath, 'r') as inf, open(outpath, 'w') as outf:
            # skip the first '{"lineItems": "' characters
            inf.seek(offset_beginning)
            while True:
                chunk = inf.read(chunksize)
                if len(chunk) < chunksize:
                    # we are at the end and need to strip the "} characters
                    outf.write(chunk[:offset_tail])
                    break
                else:
                    outf.write(chunk)
        return outpath

    def download_and_clean_lineitems(self, outpath, filter_type, filter_ids=None):
        tmp_outpath = '/tmp/temp_{}_raw_lineitems.json'.format(random.randint(0,999999))
        self._download_lineitems(tmp_outpath, filter_type, filter_ids)
        real_outpath = self._clean_lineitems_response_via_ijson(tmp_outpath, outpath)
        return real_outpath


def validate_extractor_params(params):
    schema = vp.Schema(
        {
            "extract": {
                "lineItems": {
                    "filterType": vp.Any("ADVERTISER_ID", "INSERTION_ORDER_ID", "LINE_ITEM_ID"),
                    vp.Optional("filterIds"): [vp.Coerce(int)]
                }
            }
        }
    )
    return schema(params)

def columnize_filter_type(word):
    """
    >>> filter_type_to_column_name("LINE_ITEM_ID")
    "Line_Item_Id"

    The api returns columns like "Line Item Id"
    in storage this will be "Line_Item_Id"
    """
    return '_'.join(map(lambda w: w.capitalize(), word.split('_')))

def write_manifest(outpath, manifest):
    logging.debug("Writing manifest %s", outpath)
    with open(outpath, 'w') as outf:
        json.dump(manifest, outf)

def main(datadir, credentials, params):
    params_cleaned = validate_extractor_params(params)
    ex = DBMExtractor(**credentials)
    config_lineitems = params_cleaned['extract']['lineItems']
    outpath = Path(datadir) / 'out/tables/{}.csv'.format(config_lineitems['filterType'].lower())
    ex.download_and_clean_lineitems(outpath,
                                    config_lineitems['filterType'],
                                    config_lineitems.get('filterIds'))

    manifest_path = str(outpath) + '.manifest'
    write_manifest(
        manifest_path,
        {
            "incremental": True,
            "primary_key": columnize_filter_type(config_lineitems['filterType'])
        }
    )

