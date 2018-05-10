import logging
import os
import sys
import requests
from keboola.docker import Config
import exdbm.extractor
import voluptuous as vp

if __name__ == '__main__':
    try:
        datadir = os.environ['KBC_DATADIR']
        config = Config(datadir)
        params = config.get_parameters()
        if params.get('debug'):
            logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
        else:
            logging.basicConfig(level=logging.INFO, stream=sys.stdout)

        credentials = {
            'client_id': config.get_oauthapi_appkey(),
            'client_secret': config.get_oauthapi_appsecret(),
            'refresh_token': config.get_oauthapi_data()['refresh_token']
        }
        exdbm.extractor.main(datadir, credentials, params)
    except (ValueError, KeyError, vp.MultipleInvalid):
        logging.error(err)
        sys.exit(1)
    except requests.HTTPError as err:
        logging.error("%s %s", err, err.response.text)
        sys.exit(1)
    except:
        logging.exception("Internal error")
        sys.exit(2)
