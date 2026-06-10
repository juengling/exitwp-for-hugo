import pytest
from internal.amazon import is_amazon_link
from internal.amazon_utils import is_valid_amazon_url, is_valid_amazon_url


# -----------------------------
# Tests for is_amazon_link
# -----------------------------

def test_is_amazon_link_invalid_url():
    # invalid URL triggers urlparse exception → should return False
    assert is_amazon_link("http://[::1") is False


def test_is_amazon_link_shortlink():
    assert is_amazon_link("https://amzn.to/xyz") is True


def test_is_amazon_link_smile():
    assert is_amazon_link("https://smile.amazon.de/dp/B00ABC1234") is True


def test_is_amazon_link_mobile():
    assert is_amazon_link("https://m.amazon.de/dp/B00ABC1234") is True


def test_is_amazon_link_www():
    assert is_amazon_link("https://www.amazon.de/dp/B00ABC1234") is True


def test_is_amazon_link_non_amazon():
    assert is_amazon_link("https://example.com") is False


# -----------------------------
# Tests for is_valid_amazon_url
# -----------------------------

def test_is_valid_amazon_url_shortlink():
    assert is_valid_amazon_url("https://amzn.to/xyz") is True


def test_is_valid_amazon_url_no_asin():
    assert is_valid_amazon_url("https://amazon.de/s?k=usb") is False


def test_is_valid_amazon_url_offer_listing():
    assert is_valid_amazon_url("https://amazon.de/gp/offer-listing/B00ABC1234") is True


def test_is_valid_amazon_url_dash_dp():
    assert is_valid_amazon_url("https://amazon.de/-/dp/B00ABC1234") is True
