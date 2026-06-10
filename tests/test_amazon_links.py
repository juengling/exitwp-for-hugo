import pytest
from internal.amazon import is_amazon_link, process_amazon_link
from internal.amazon_utils import is_valid_amazon_url, clean_amazon_url


# ---------------------------------------------------------
# is_amazon_link – valid Amazon URLs
# ---------------------------------------------------------

@pytest.mark.parametrize("url", [
    # Standard Amazon domains
    "https://amazon.de/dp/B00ABC1234",
    "https://www.amazon.com/gp/product/B00ABC1234",
    "https://amazon.co.uk/dp/B00ABC1234",
    "https://amazon.fr/dp/B00ABC1234",

    # Smile
    "https://smile.amazon.de/dp/B00ABC1234",
    "https://smile.amazon.com/gp/product/B00ABC1234",

    # Mobile
    "https://m.amazon.de/dp/B00ABC1234",

    # With port
    "https://amazon.de:443/dp/B00ABC1234",

    # Mixed case
    "HTTP://AMAZON.DE/dp/B00ABC1234",
    "https://AMAZON.COM/dp/B00ABC1234",

    # Shortlinks (valid)
    "https://amzn.to/3XYZabc",
    "http://amzn.to/xyz",
])
def test_is_amazon_link_true(url):
    assert is_amazon_link(url) is True


# ---------------------------------------------------------
# is_amazon_link – invalid URLs
# ---------------------------------------------------------

@pytest.mark.parametrize("url", [
    None,
    "",
    "   ",
    "javascript:alert(1)",
    "http:///nohost",
    "https://example.com",
    "https://www.amzn.to/xyz",   # NOT a valid Amazon shortlink
])
def test_is_amazon_link_false(url):
    assert is_amazon_link(url) is False


# ---------------------------------------------------------
# is_valid_amazon_url – valid product URLs
# ---------------------------------------------------------

@pytest.mark.parametrize("url", [
    "https://amazon.de/dp/B00ABC1234",
    "https://www.amazon.com/gp/product/B00ABC1234",
    "https://amazon.co.uk/gp/offer-listing/B00ABC1234",
    "https://amazon.fr/-/dp/B00ABC1234",
    "https://amzn.to/xyz",  # shortlinks always valid
])
def test_is_valid_amazon_url_true(url):
    assert is_valid_amazon_url(url) is True


# ---------------------------------------------------------
# is_valid_amazon_url – invalid product URLs
# ---------------------------------------------------------

@pytest.mark.parametrize("url", [
    "https://amazon.de/s?k=usb",          # no ASIN
    "https://amazon.com/",                # no ASIN
    "https://example.com/dp/B00ABC1234",  # not Amazon
])
def test_is_valid_amazon_url_false(url):
    assert is_valid_amazon_url(url) is False

def test_clean_amazon_url_non_amazon_domain():
    url = "https://example.com/foo/bar"
    assert clean_amazon_url(url) == url

def test_clean_amazon_url_amazon_no_asin():
    url = "https://www.amazon.de/s?k=python"
    assert clean_amazon_url(url) == url

def test_clean_amazon_url_with_asin():
    url = "https://www.amazon.de/gp/product/b012345678/"
    assert clean_amazon_url(url) == "https://amazon.de/dp/B012345678"

def test_process_amazon_link_invalid_amazon_url_keep():
    url = "https://www.amazon.de/s?k=python"  # Amazon, aber ohne ASIN → ungültig
    assert process_amazon_link(url, "keep") == url

def test_process_amazon_link_invalid_amazon_url_remove():
    url = "https://www.amazon.de/s?k=python"
    assert process_amazon_link(url, "remove") == ""

def test_process_amazon_link_invalid_amazon_url_keep():
    url = "https://www.amazon.de/s?k=python"  # Amazon, aber ohne ASIN → ungültig
    assert process_amazon_link(url, "keep") == url

def test_process_amazon_link_unknown_mode():
    url = "https://www.amazon.de/dp/B012345678"
    assert process_amazon_link(url, "unknown") == url
