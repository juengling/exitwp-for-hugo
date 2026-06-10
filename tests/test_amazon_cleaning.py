import pytest
from internal.amazon_utils import clean_amazon_url


def test_clean_amazon_url_no_asin():
    # No ASIN → URL must remain unchanged
    url = "https://amazon.de/s?k=usb"
    assert clean_amazon_url(url) == url


def test_clean_amazon_url_gp_product():
    assert clean_amazon_url("https://www.amazon.co.jp/gp/product/B00ABC1234") \
        == "https://amazon.co.jp/dp/B00ABC1234"


def test_clean_amazon_url_offer_listing():
    assert clean_amazon_url("https://amazon.es/gp/offer-listing/B00ABC1234") \
        == "https://amazon.es/dp/B00ABC1234"


def test_clean_amazon_url_uppercase_domain():
    assert clean_amazon_url("https://AMAZON.DE/dp/B00ABC1234") \
        == "https://amazon.de/dp/B00ABC1234"
