import pytest
from exdbm.extractor import validate_extractor_params
import voluptuous as vp

def test_validating_config_with_filter_ids():
    cfg = {
        "extract": {
            "lineItems": [
                {
                    "filterType": "ADVERTISER_ID",
                    "filterIds": [12, "23", 34]
                }
            ]
        }
    }
    validate_extractor_params(cfg)

def test_validating_config_without_filter_ids():
    cfg = {
        "extract": {
            "lineItems": [
                {
                    "filterType": "ADVERTISER_ID",
                }
            ]
        }
    }
    validate_extractor_params(cfg)


def test_validating_config_multiple_filter_types():
    cfg = {
        "extract": {
            "lineItems": [
                {
                    "filterType": "ADVERTISER_ID",
                },
                {
                    "filterType": "LINE_ITEM_ID",
                }
            ]
        }
    }
    validate_extractor_params(cfg)


def test_validating_config_invalid_filter_type():
    cfg = {
        "extract": {
            "lineItems": [
                {
                    "filterType": "INVALID",
                }
            ]
        }
    }
    with pytest.raises(vp.MultipleInvalid):
        validate_extractor_params(cfg)
