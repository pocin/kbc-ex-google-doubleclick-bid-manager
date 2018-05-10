# Keboola extractor for Google Doubleclick Bid Manager
---
[![Build Status](https://travis-ci.org/pocin/kbc-ex-google-doubleclick-bid-manager.svg?branch=master)](https://travis-ci.org/pocin/kbc-ex-google-doubleclick-bid-manager)
----

# Config

Uses this endpoint https://developers.google.com/bid-manager/v1/lineitems/downloadlineitems for downloading line items in CSV format.

`config.json` 

```javascript
{
  "extract": {
    "lineItems": [
      {
        "filterType": "LINE_ITEM_ID",
        "filterIds": [1,2,3]
      }
    ]
    }
}

```

- `filterType` is one of `"ADVERTISER_ID", "INSERTION_ORDER_ID", "LINE_ITEM_ID"`
- `filterIds` is an array of integers. Omit if you want to download all items

the table will be downloaded to `/data/out/tables/{filterType}.csv` (incremental loading is turned on)

# Development

create `.env` file based on `.env_template` in the root of this repo.

https://developers.google.com/api-client-library/python/apis/doubleclickbidmanager/v1
https://github.com/googleads/googleads-bidmanager-examples/blob/master/python/util.py
